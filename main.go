package main

import (
	"log"
	"net/http"

	"github.com/ccutch/ccutch-blog/backend"
	"github.com/ccutch/ccutch-blog/frontend"

	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	frontend.BindViewRoutes(router)
	backend.BindAPIRoutes(router)
	http.Handle("/", router)

	log.Println("Starting server on port 8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
