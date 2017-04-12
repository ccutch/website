package backend

import (
	"fmt"

	"cloud.google.com/go/datastore"
	"github.com/asaskevich/govalidator"
	"golang.org/x/net/context"
)

var datastoreClient *datastore.Client

func init() {
	var err error
	var ctx = context.Background()

	if datastoreClient, err = datastore.NewClient(ctx, "ccutch-blog"); err != nil {
		panic(err)
	}
}

// Post is a blog post
type Post struct {
	ID    string `json:"id"`
	Title string `json:"title"`
	Body  string `json:"body"`
}

// Validate fields of post
func (p *Post) Validate() error {
	if govalidator.IsNull(p.Title) || govalidator.IsNull(p.Body) {
		return fmt.Errorf("Invalid Post data %v", p)
	}
	return nil
}
