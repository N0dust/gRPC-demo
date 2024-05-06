package client

import (
	"context"
	"gRPC-demo/pb/product"
	"github.com/pkg/errors"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var client product.ProductServiceClient

func InitClient(target string) error {
	credentials := insecure.NewCredentials()
	conn, err := grpc.Dial(target, grpc.WithTransportCredentials(credentials))
	if err != nil {
		panic(err)
	}
	client = product.NewProductServiceClient(conn)
	return nil
}

func GetProduct(ctx context.Context, id string) (*product.Product, error) {
	req := product.ProductReq{Id: id}
	resp, err := client.GetProduct(ctx, &req)
	if resp != nil {
		return resp.Product, err
	}
	return nil, err
}

func CreateProduct(ctx context.Context, p *product.Product) error {
	if p == nil {
		return errors.New("product is empty")
	}
	req := product.ProductReq{Product: p, Id: p.Id}
	resp, err := client.CreateProduct(ctx, &req)
	if err == nil {
		return err
	}
	if resp != nil {
		err = errors.WithMessage(err, resp.Msg)
	}
	return err
}

func DeleteProduct(ctx context.Context, id string) error {
	req := product.ProductReq{Id: id}
	resp, err := client.DeleteProduct(ctx, &req)
	if err == nil {
		return err
	}
	if resp != nil {
		err = errors.WithMessage(err, resp.Msg)
	}
	return err
}
