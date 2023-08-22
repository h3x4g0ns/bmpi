package main

import (
	"database/sql"
	"encoding/json"
	"net/http"
	"os"

	"github.com/gorilla/sessions"
)

var (
	store = sessions.NewFilesystemStore("./sessiondata", []byte(os.Getenv("SECRET-KEY")))
)

func init() {
	store.Options = &sessions.Options{
		Path:     "/",
		MaxAge:   86400 * 7, // 1 week
		HttpOnly: true,
	}
}

func (h *AuthHandler) registerHandler(w http.ResponseWriter, r *http.Request) {
	username := r.FormValue("username")
	password := r.FormValue("password")

	salt := generateSalt()
	hashedPassword := hashPasswordWithSalt(password, salt)

	statement, _ := h.db.Prepare("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)")
	statement.Exec(username, hashedPassword, salt)
	w.Write([]byte("User registered successfully!"))
}

func (h *AuthHandler) LoginHandler(w http.ResponseWriter, r *http.Request) {
	username := r.FormValue("username")
	password := r.FormValue("password")

	row := h.db.QueryRow("SELECT password, salt FROM users WHERE username=?", username)

	var retrievedHashedPassword, salt string
	if err := row.Scan(&retrievedHashedPassword, &salt); err == sql.ErrNoRows {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("Invalid credentials"))
		return
	}

	// Hash the provided password with the retrieved salt and compare
	if hashPasswordWithSalt(password, salt) == retrievedHashedPassword {
		session, _ := store.Get(r, "session-name")
		sessionToken := generateSessionToken()
		session.Values["session_token"] = sessionToken
		session.Save(r, w)
		jsonResponse, _ := json.Marshal(map[string]string{"session_token": sessionToken})
		w.Write(jsonResponse)
	} else {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("Invalid credentials"))
	}
}

func HelloWorldHandler(w http.ResponseWriter, r *http.Request) {
	sessionToken := r.Header.Get("Session-Token")
	if sessionToken == "" {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("No session token provided"))
		return
	}

	session, _ := store.Get(r, "session-name")
	storedSessionToken, found := session.Values["session_token"]
	if !found || storedSessionToken != sessionToken {
		w.WriteHeader(http.StatusUnauthorized)
		w.Write([]byte("Invalid session token"))
		return
	}

	w.Write([]byte("Hello!"))
}
