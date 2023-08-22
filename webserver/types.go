package main

import (
	"database/sql"
)

type AuthHandler struct {
	db *sql.DB
}
