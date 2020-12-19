// Receives POST request with json data,  and run visualization program accordingly

package main
import (
    "encoding/json"
    "log"
	"net/http"
	"os"
	"strings"
)

var procs []int
var cmd Any 


type JsonFormat struct {
	Arg1 *[]int `json:"component"`
	Arg2 *int `json:"effect"`
}

type Any interface{}

// When server receives an effect for particuliar strips, kills anything displaying on that strip
func KillProcs(sub Any) {
	sub.Process.Kill()


// Display the selected pattern on the range of selected devices
func (j JsonFormat, url string) SubProcess() {
	KillProcs(cmd)
	urls := strings.Join(url, " ")
	cmd = exec.Command("python", "dancypi/scripts/visualization.py", j.Arg2, "urls")
}

// Handles request on the path / and input POST data into JsonFormat struct
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
	go t.SubProcess()

}


func main() {
    http.HandleFunc("/", Receiver)
    log.Fatal(http.ListenAndServe("0.0.0.0:8082", nil))
}


