// Receives POST request with json data,  and run visualization program accordingly
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os/exec"
	"strings"
)

//var procs []int
var processes []*exec.Cmd
var cmd *exec.Cmd

//JSONFormat is the Struct to input received JSON date
type JSONFormat struct {
	Arg1 *[]string `json:"component"`
	Arg2 *int      `json:"effect"`
}

//SubProcess runs the python visualization with relevant args
func SubProcess(j *JSONFormat) {

	for _, value := range processes {
		value.Process.Kill()
	}
	tmp := *j.Arg1
	effect := *j.Arg2
	urls := strings.Join(tmp, " ")
	if effect == 1 {
		cmd = exec.Command("python", "dancypi/scripts/python/visualization.py", "scroll", urls)
		//cmd = exec.Command("python3", "testgo/test1.py")
	} else if effect == 2 {
		cmd = exec.Command("python", "dancypi/scripts/python/visualization.py", "energy", urls)
		//cmd = exec.Command("python3", "testgo/test2.py")
	} else if effect == 3 {
		cmd = exec.Command("python", "dancypi/scripts/python/visualization.py", "spectrum", urls)
	}
	processes = append(processes, cmd)
	if err := cmd.Run(); err != nil {
		log.Printf("Processes killed\n")
	}
}

//Receiver is triggered on the "path" and decode JSON to input in JSONFormat
func Receiver(rw http.ResponseWriter, req *http.Request) {
	d := json.NewDecoder(req.Body)
	d.DisallowUnknownFields()
	t := new(JSONFormat)
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
	go SubProcess(t)

}

func main() {
	http.HandleFunc("/", Receiver)
	log.Fatal(http.ListenAndServe("0.0.0.0:8082", nil))
}
