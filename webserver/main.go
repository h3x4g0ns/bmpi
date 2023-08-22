package main

import (
	"database/sql"
	"log"
	"net/http"
	"webserver/handlers" // Adjust this import path as necessary

	"github.com/gorilla/mux"
	_ "github.com/mattn/go-sqlite3"
)

func initDB(filepath string) *handlers.AuthHandler {
	db, err := sql.Open("sqlite3", filepath)
	if err != nil {
		log.Fatal(err)
	}

	statement, _ := db.Prepare(`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)`)
	statement.Exec()

	authHandler := &handlers.AuthHandler{
		DB: db,
	}
	return authHandler
}

func main() {
	h := initDB("auth.db")
	r := mux.NewRouter()

	r.HandleFunc("/api/v1/creds", h.LoginHandler).Methods("POST")
	r.HandleFunc("/api/v1/hello", handlers.HelloWorldHandler).Methods("GET")

	http.Handle("/", r)
	// http.ListenAndServeTLS(":8443", "selfsigned.crt", "selfsigned.key", nil)
	http.ListenAndServe(":8000", nil)
}
