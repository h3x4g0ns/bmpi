package handlers

import (
	"database/sql"
)

type AuthHandler struct {
	DB *sql.DB
}
