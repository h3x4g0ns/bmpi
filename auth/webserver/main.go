package main

import (
	"fmt"
	"net/http"
	"time"
	"github.com/gorilla/mux"
	"github.com/gorilla/sessions"
)

var (
	key   = []byte("super-secret-key")
	store = sessions.NewCookieStore(key)
)

func main() {
	r := mux.NewRouter()

	r.HandleFunc("/login", LoginHandler).Methods("POST")
	r.HandleFunc("/validate", ValidateTokenHandler).Methods("GET")

	http.ListenAndServe(":8080", r)
}
