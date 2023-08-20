package main

import (
	"github.com/gorilla/mux"
	"net/http"
	"database/sql"
	"log"
	_ "github.com/mattn/go-sqlite3"
)

func initDB(filepath string) *AuthHandler {
	db, err := sql.Open("sqlite3", filepath)
	if err != nil {
		log.Fatal(err)
	}

	statement, _ := db.Prepare(`CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)`)
	statement.Exec()
	return db

	authHandler := &AuthHandler{
		db: db,
	}
	return authHandler
}

func main() {
	h := initDB("auth.db")
	r := mux.NewRouter()

	r.HandleFunc("/api/v1/creds", h.LoginHandler).Methods("POST")
	r.HandleFunc("/api/v1/hello", HelloWorldHandler).Methods("GET")

	http.Handle("/", r)
	http.ListenAndServeTLS(":8443", "selfsigned.crt", "selfsigned.key", nil)
}
