package main

import (
	context "context"
	"fmt"
	"log"
	"net"

	grpc "google.golang.org/grpc"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

var (
	db *gorm.DB
)

// GroupService struct IS tesgot for rpc
type GroupService struct{}

// UserGroup struct IS tesgot for rpc
type UserGroup struct {
	GroupID   string `json:"group_id" gorm:"primaryKey"`
	GroupName string `json:"group_name"`
}

// ConnectDB  IS tes
func ConnectDB() {
	dsn := "root:@tcp(127.0.0.1:3306)/test?charset=utf8mb4&parseTime=True&loc=Local"
	database, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		fmt.Println(err)
	} else {
		db = database
	}
	db.AutoMigrate(&UserGroup{})
	fmt.Printf("connet succeed %v", db)
}

// CreateGroup struct IS test for rpc
func (GroupService *GroupService) CreateGroup(ctx context.Context, req *GroupRequest) (*Result, error) {
	group := new(UserGroup)
	result := new(Result)

	group.GroupID = req.GroupID
	group.GroupName = req.GroupName

	if DbResult := db.Create(&group); DbResult.Error != nil {
		result.Status = false
		return result, DbResult.Error
	}

	result.Status = true
	result.GroupID = req.GetGroupID()
	result.GroupName = req.GetGroupName()
	log.Println(result)
	return result, nil

	//return nil, status.Errorf(codes.Unimplemented, "method CreateGroup not implemented")
}

// GetGroup struct IS test for rpc
func (GroupService *GroupService) GetGroup(ctx context.Context, req *GroupRequest) (*Result, error) {
	result := new(Result)
	group := new(UserGroup)
	// db.Where("groupid = ?", req.GroupID).First(&group)

	if DbResult := db.Where("groupid = ?", req.GroupID).First(&group); DbResult.Error != nil {
		result.Status = false
		return result, DbResult.Error
	}

	result.Status = true
	result.GroupID = group.GroupID
	result.GroupName = group.GroupName
	log.Println(result)
	return result, nil

	// return nil, status.Errorf(codes.Unimplemented, "method GetGroup not implemented")
}

// DeleteGroup struct IS test for rpc
func (GroupService *GroupService) DeleteGroup(ctx context.Context, req *GroupRequest) (*Result, error) {
	result := new(Result)
	group := new(UserGroup)
	if DbResult := db.Where("groupid = ?", req.GroupID).Delete(&group); DbResult.Error != nil {
		result.Status = false
		return result, DbResult.Error
	}

	result.Status = true
	log.Println(result)
	return result, nil

	// return nil, status.Errorf(codes.Unimplemented, "method DeleteGroup not implemented")
}

func main() {
	ConnectDB()
	grpcServer := grpc.NewServer()
	RegisterGroupServiceServer(grpcServer, new(GroupService))

	listener, err := net.Listen("tcp", ":8090")
	if err != nil {
		log.Fatal("ListenTCP error:", err)
	}
	grpcServer.Serve(listener)

}
