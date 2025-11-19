package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/buger/jsonparser"
)

var users = map[string]struct {
	Password string
	Roles    []string
}{
	"daniel": {"1234", []string{"moderator", "viewer"}},
	"root":   {"toor", []string{"admin"}},
}

func contains(slice []string, target string) bool {
	for _, r := range slice {
		if r == target {
			return true
		}
	}
	return false
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, `{"error":"cannot read body"}`, http.StatusBadRequest)
		return
	}

	user, err1 := jsonparser.GetString(body, "user")
	pass, err2 := jsonparser.GetString(body, "password")
	role, err3 := jsonparser.GetString(body, "role")
	if err1 != nil || err2 != nil || err3 != nil {
		http.Error(w, `{"error":"invalid JSON fields"}`, http.StatusBadRequest)
		return
	}

	u, ok := users[user]
	if !ok || u.Password != pass {
		http.Error(w, `{"error":"invalid credentials"}`, http.StatusUnauthorized)
		return
	}

	if !contains(u.Roles, role) {
		http.Error(w, `{"error":"role not allowed"}`, http.StatusForbidden)
		return
	}

	resp, err := http.Post("http://lab1-python:5000/internal",
		"application/json",
		bytes.NewReader(body))
	if err != nil {
		http.Error(w, fmt.Sprintf(`{"error":"internal error: %s"}`, err), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	data, _ := io.ReadAll(resp.Body)

	for k, v := range resp.Header {
		for _, vv := range v {
			w.Header().Add(k, vv)
		}
	}
	w.WriteHeader(resp.StatusCode)
	w.Write(data)
}

func main() {
	http.HandleFunc("/login", loginHandler)
	fmt.Println("Go backend listening on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
