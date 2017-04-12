package frontend

import (
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

var indexFile []byte

// BindViewRoutes rendering html and serves static files
func BindViewRoutes(router *mux.Router) {
	router.NewRoute().Path("/").HandlerFunc(serveIndexFile)
}

func serveIndexFile(w http.ResponseWriter, r *http.Request) {
	if len(indexFile) == 0 {
		b, err := ioutil.ReadFile("frontend/index.html")
		if err != nil {
			log.Fatal(err)
		}
		indexFile = b
	}
	w.Write(indexFile)
}
