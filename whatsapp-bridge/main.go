package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/mdp/qrterminal/v3"
	"go.mau.fi/whatsmeow"
	waProto "go.mau.fi/whatsmeow/binary/proto"
	"go.mau.fi/whatsmeow/store/sqlstore"
	"go.mau.fi/whatsmeow/types"
	waLog "go.mau.fi/whatsmeow/util/log"
	"google.golang.org/protobuf/proto"
	_ "modernc.org/sqlite"
)

type sendRequest struct {
	Recipient string `json:"recipient"`
	Message   string `json:"message"`
}

type sendResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
}

type healthResponse struct {
	Status    string `json:"status"`
	Connected bool   `json:"connected"`
	LoggedIn  bool   `json:"logged_in"`
}

var client *whatsmeow.Client

func normalizeRecipient(raw string) (string, error) {
	recipient := strings.TrimSpace(raw)
	recipient = strings.TrimPrefix(recipient, "+")
	recipient = strings.ReplaceAll(recipient, " ", "")
	recipient = strings.ReplaceAll(recipient, "-", "")
	recipient = strings.ReplaceAll(recipient, "(", "")
	recipient = strings.ReplaceAll(recipient, ")", "")

	matched, _ := regexp.MatchString(`^[0-9]{8,15}$`, recipient)
	if !matched {
		return "", fmt.Errorf("recipient must be an international phone number like 923001234567")
	}

	return recipient, nil
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, healthResponse{
		Status:    "ok",
		Connected: client != nil && client.IsConnected(),
		LoggedIn:  client != nil && client.IsLoggedIn(),
	})
}

func sendHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, sendResponse{
			Success: false,
			Message: "method not allowed",
		})
		return
	}

	r.Body = http.MaxBytesReader(w, r.Body, 1<<20)

	var req sendRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, sendResponse{
			Success: false,
			Message: "invalid JSON body",
		})
		return
	}

	recipient, err := normalizeRecipient(req.Recipient)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, sendResponse{
			Success: false,
			Message: err.Error(),
		})
		return
	}

	message := strings.TrimSpace(req.Message)
	if message == "" {
		writeJSON(w, http.StatusBadRequest, sendResponse{
			Success: false,
			Message: "message is required",
		})
		return
	}

	if client == nil || !client.IsConnected() || !client.IsLoggedIn() {
		writeJSON(w, http.StatusServiceUnavailable, sendResponse{
			Success: false,
			Message: "WhatsApp bridge is not connected. Restart and scan QR if needed.",
		})
		return
	}

	target := types.NewJID(recipient, types.DefaultUserServer)

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	_, err = client.SendMessage(ctx, target, &waProto.Message{
		Conversation: proto.String(message),
	})
	if err != nil {
		writeJSON(w, http.StatusBadGateway, sendResponse{
			Success: false,
			Message: err.Error(),
		})
		return
	}

	writeJSON(w, http.StatusOK, sendResponse{
		Success: true,
		Message: "message sent",
	})
}

func main() {
	ctx := context.Background()

	storeDir := filepath.Join(".", "store")
	if err := os.MkdirAll(storeDir, 0o755); err != nil {
		panic(err)
	}

	dbLog := waLog.Stdout("Database", "INFO", true)
	container, err := sqlstore.New(
		ctx,
		"sqlite",
		"file:store/whatsapp.db?_pragma=foreign_keys(1)&_pragma=journal_mode(WAL)&_pragma=busy_timeout(15000)",
		dbLog,
	)
	if err != nil {
		panic(err)
	}

	deviceStore, err := container.GetFirstDevice(ctx)
	if err != nil {
		panic(err)
	}

	clientLog := waLog.Stdout("Client", "INFO", true)
	client = whatsmeow.NewClient(deviceStore, clientLog)

	if client.Store.ID == nil {
		qrChan, err := client.GetQRChannel(ctx)
		if err != nil {
			panic(err)
		}

		if err := client.Connect(); err != nil {
			panic(err)
		}

		for evt := range qrChan {
			if evt.Event == "code" {
				fmt.Println("Scan this QR in WhatsApp > Linked Devices:")
				qrterminal.GenerateHalfBlock(evt.Code, qrterminal.L, os.Stdout)
			} else {
				fmt.Println("Login event:", evt.Event)
			}
		}
	} else {
		if err := client.Connect(); err != nil {
			panic(err)
		}
	}

	http.HandleFunc("/health", healthHandler)
	http.HandleFunc("/send", sendHandler)

	fmt.Println("WhatsApp bridge running on http://127.0.0.1:8080")
	if err := http.ListenAndServe("127.0.0.1:8080", nil); err != nil {
		panic(err)
	}
}
