package main

import (
	"database/sql"
)

type AppHandler struct {
	db *sql.DB
}