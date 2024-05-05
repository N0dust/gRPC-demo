package main

import (
	"context"
	"errors"
	"gRPC-demo/pb/product"
	"log"
	"net"

	grpc "google.golang.org/grpc"
)

var cacheTable = make(map[string]*product.Product)

type ProductService struct {
	*product.UnimplementedProductServiceServer
}

func (s *ProductService) CreateProduct(ctx context.Context, req *product.ProductReq) (*product.ProductResp, error) {
	result := new(product.ProductResp)
	var err error
	_, ok := cacheTable[req.Id]
	if ok {
		err = errors.New("already create " + req.Id)
	}
	if req.Product == nil {
		err = errors.New("product is empty")
	}
	if err != nil {
		result.Success = false
		result.Msg = err.Error()
		return result, err
	}

	cacheTable[req.Id] = req.Product
	result.Success = true
	return result, nil
}

func (s *ProductService) GetProduct(ctx context.Context, req *product.ProductReq) (*product.ProductResp, error) {
	result := new(product.ProductResp)
	p, ok := cacheTable[req.Id]
	if !ok {
		err := errors.New("no result")
		result.Success = false
		result.Msg = err.Error()
		return result, err
	}
	result.Product = p
	result.Success = true

	return result, nil
}

func (s *ProductService) DeleteProduct(ctx context.Context, req *product.ProductReq) (*product.ProductResp, error) {
	result := new(product.ProductResp)
	delete(cacheTable, req.Id)
	result.Success = true
	return result, nil
}

func main() {
	grpcServer := grpc.NewServer()
	product.RegisterProductServiceServer(grpcServer, new(ProductService))

	listenPort := "8090"
	log.Println("grpcServer listening at " + "127.0.0.1:" + listenPort)
	listener, err := net.Listen("tcp", ":"+listenPort)
	if err != nil {
		log.Fatal("ListenTCP error:", err)
	}
	grpcServer.Serve(listener)
}
