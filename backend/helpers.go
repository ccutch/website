package backend

import (
	"encoding/json"
	"net/http"
)

func parseBody(r *http.Request, v interface{}) interface{} {
	d := json.NewDecoder(r.Body)
	d.Decode(v)
	return v
}

func serveJSON(w http.ResponseWriter, v interface{}) {
	e := json.NewEncoder(w)
	e.Encode(v)
}
