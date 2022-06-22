package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

func main() {
	http.HandleFunc("/api/v1", getuser)
	s := &http.Server{
		Addr:           ":8080",
		ReadTimeout:    30 * time.Second,
		WriteTimeout:   30 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	log.Fatal(s.ListenAndServe())
}

func getuser(w http.ResponseWriter, r *http.Request) {
	marshal, _ := json.Marshal(getuser_json())
	w.Write(marshal)
}

func ConnectDB() *gorm.DB {
	var err error
	//dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8mb4&parseTime=True&loc=Local", conf.User, conf.Password, conf.Host, conf.DbName),
	dsn := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8mb4&parseTime=True&loc=Local", "root", "A9******f", "192.xxx.xxx.xx:3306", "aliyun")

	DB, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic(err)
	}
	sqldb, err := DB.DB()
	if err != nil {
		panic(err)
	}
	sqldb.SetMaxIdleConns(10)
	sqldb.SetMaxOpenConns(200)
	sqldb.SetConnMaxLifetime(60 * time.Second)
	//DB.ShowSQL(true)
	err = sqldb.Ping()
	if err != nil {
		panic(err)
	}
	fmt.Println("mysql connection successful")
	return DB
}
func getuser_json() []pkpk {
	db := ConnectDB()
	var datas []pkpk

	err := db.Debug().Table("pkpk").Find(&datas).Error

	if err != nil {
		panic(err.Error())
	}
	return datas
}

type pkpk struct {
	CreationTime     string
	SerialNumber     string
	Status           string
	InstanceId       string
	Description      string
	InstanceName     string
	RegionId         string
	ZoneId           string
	InstanceType     string
	OSNameEn         string
	OSType           string
	Cpu              string
	Memory           string
	ExpiredTime      string
	PrimaryIpAddress string
	ipAddress        string
}
