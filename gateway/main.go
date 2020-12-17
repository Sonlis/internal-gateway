package main
import (
    "encoding/json"
    "log"
	"net/http"
	"./sender"
)

type JsonFormat struct {
	Arg1 *int `json:"component"`
	Arg2 *int `json:"effect"`
}


func (j JsonFormat) Router() string {
	var url string
	switch j.Arg1 {
	case 1: url = ""
	case 2: url = ""
	case 3: url = ""
	default: return "Wrong argument"
	}
	Sender(j, url)
}

func (j JsonFormat, url string) Sender() {
	if j.Arg1 = 1 {
		switch j.Arg2:
		case 1:
		case 2: 
		case 3:
	}
	req, err := http.NewRquest("GET", "")
}


func Receiver(rw http.ResponseWriter, req *http.Request) {
	d := json.NewDecoder(req.Body)
	d.DisallowUnknownFields()
	t := new(JsonFormat)
	err := d.Decode(&t)
	if err != nil {
    	http.Error(rw, err.Error(), http.StatusBadRequest)
    return
	}
	if t.Arg1 == nil {
    	http.Error(rw, "missing field 'test' from JSON object", http.StatusBadRequest)
    return
	}
	if d.More() {
    	http.Error(rw, "extraneous data after JSON object", http.StatusBadRequest)
    return
	}
	log.Println(*t.Arg1)
	log.Println(*t.Arg2)
	go t.Router()

}


func main() {
    http.HandleFunc("/", Route)
    log.Fatal(http.ListenAndServe("0.0.0.0:8082", nil))
}