package backend

import (
	"net/http"

	"github.com/gorilla/mux"
)

// Route in api
type Route struct {
	Path        string
	Description string
	Actions     map[string]http.HandlerFunc
}

var routes = []Route{
	postListRoute,
	postRoute,
}

// BindAPIRoutes creates router mux to http
func BindAPIRoutes(router *mux.Router) {
	apiRouter := router.PathPrefix("/api").Subrouter().StrictSlash(true)

	for _, route := range routes {
		for m, a := range route.Actions {
			apiRouter.NewRoute().
				Methods(m).
				Path(route.Path).
				HandlerFunc(a)
		}
	}

}
