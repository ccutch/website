package backend

import (
	"net/http"

	"google.golang.org/api/iterator"

	"golang.org/x/net/context"

	"cloud.google.com/go/datastore"
	"github.com/gorilla/mux"
	"github.com/satori/go.uuid"
)

var (
	postListRoute = Route{
		Path:        "/posts",
		Description: "REST handler for listing and creating posts",
		Actions: map[string]http.HandlerFunc{
			"GET":  listPosts,
			"POST": createPost,
		},
	}

	postRoute = Route{
		Path:        "/posts/{postID:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}}",
		Description: "REST handler getting, updating, and deleting posts",
		Actions: map[string]http.HandlerFunc{
			"GET": getPost,
			"PUT": updatePost,
		},
	}
)

func listPosts(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	q := datastore.NewQuery("Post")
	iter := datastoreClient.Run(ctx, q)
	posts := []Post{}

	for {
		var post Post
		_, err := iter.Next(&post)

		if err == iterator.Done {
			break
		}

		if err != nil {
			http.Error(w, "Error fetching post: "+err.Error(), http.StatusInternalServerError)
			return
		}

		posts = append(posts, post)
	}
	serveJSON(w, posts)
}

func getPost(w http.ResponseWriter, r *http.Request) {
	postID := mux.Vars(r)["postID"]

	ctx := context.Background()
	key := datastore.NameKey("Post", postID, nil)
	var post Post
	datastoreClient.Get(ctx, key, &post)
	serveJSON(w, post)
}

func updatePost(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	postID := mux.Vars(r)["postID"]
	post := parseBody(r, new(Post)).(*Post)
	post.ID = postID

	if err := post.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	key := datastore.NameKey("Post", postID, nil)
	datastoreClient.Put(ctx, key, post)
	serveJSON(w, post)
}

func createPost(w http.ResponseWriter, r *http.Request) {
	ctx := context.Background()
	post := parseBody(r, new(Post)).(*Post)
	post.ID = uuid.NewV4().String()

	if err := post.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	key := datastore.NameKey("Post", post.ID, nil)
	datastoreClient.Put(ctx, key, post)
	serveJSON(w, post)
}
