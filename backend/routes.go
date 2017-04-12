package ccutch

import (
	"fmt"
	"net/http"
)

func ApplyRoutes() {
	http.HandleFunc(testRoute)
}

func testRoute(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "test")
}
