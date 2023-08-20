package main

import (
	"fmt"
	"net/http"
	"time"
	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
)

func LoginHandler(w http.ResponseWriter, r *http.Request) {
	username := r.FormValue("username")
	password := r.FormValue("password")

	// Basic validation
	if username == "admin" && password == "password" {
		session, _ := store.Get(r, "session-name")

		// Set user as authenticated
		session.Values["authenticated"] = true

		// Set the session to expire after a week
		session.Options = &sessions.Options{
			Path:     "/",
			MaxAge:   int((7 * 24 * time.Hour).Seconds()), // 1 week
			HttpOnly: true,
		}
		session.Save(r, w)

		w.WriteHeader(http.StatusOK)
		fmt.Fprint(w, "Logged in successfully")
		return
	}

	w.WriteHeader(http.StatusUnauthorized)
	fmt.Fprint(w, "Authentication failed")
}

func ValidateTokenHandler(w http.ResponseWriter, r *http.Request) {
	session, _ := store.Get(r, "session-name")

	// Check if user is authenticated
	if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
		http.Error(w, "Forbidden", http.StatusForbidden)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Session token is valid")
}
