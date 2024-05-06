package client

import (
	"context"
	"encoding/json"
	"fmt"
	"gRPC-demo/pb/product"
	"testing"
)

func TestCreateProduct(t *testing.T) {
	_ = InitClient("127.0.0.1:8090")
	ctx := context.Background()
	skus := make([]*product.Sku, 0)
	sku := product.Sku{
		Size:  "XL",
		Price: 249,
	}
	skus = append(skus, &sku)
	p := product.Product{Id: "one", Title: "FirstTitle", Skus: skus}

	err := CreateProduct(ctx, &p)
	if err != nil {
		t.Fatal(err)
	}
}

func TestGetProduct(t *testing.T) {
	_ = InitClient("127.0.0.1:8090")
	ctx := context.Background()
	p, err := GetProduct(ctx, "one")
	if err != nil {
		t.Fatal(err)
	}
	byteData, _ := json.Marshal(p)
	fmt.Println(string(byteData))
}

func TestDeleteProduct(t *testing.T) {
	_ = InitClient("127.0.0.1:8090")
	ctx := context.Background()
	err := DeleteProduct(ctx, "one")
	if err != nil {
		t.Fatal(err)
	}
}
