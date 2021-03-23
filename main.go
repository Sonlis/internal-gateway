// Receives POST request with json data,  and run visualization program accordingly
package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os/exec"
	"strings"
	"os"
	"io/ioutil"
)

var processes []*exec.Cmd
var cmd *exec.Cmd

//JSONFormat is the Struct to input received JSON data
type JSONFormat struct {
	Arg1 *[]string `json:"component"`
	Arg2 *int      `json:"effect"`
}

//SubProcess runs the python visualization with relevant args
func SubProcess(j *JSONFormat) {

	if processes != nil {
		for _, value := range processes {
			err := value.Process.Kill()
			if err != nil {
				log.Printf("error killing processes: %v", err)
			}
		}
	}
	processes = nil 
	tmp := *j.Arg1
	effect := *j.Arg2
	urls := strings.Join(tmp, ",")
	log.Println("urls:", urls)
	file, err := os.Open("dancypi/python/config.py")
	data, err := ioutil.ReadAll(file)
		if err != nil {
			log.Printf("error reading file: %v", err)
		}
	lines := strings.Split(string(data), "\n")
	for i, line := range lines {
		if strings.Contains(line, "UDP_IP") {
			lines[i] = "UDP_IP = [" + urls + "]"
		}
	}
	output := strings.Join(lines, "\n")
	err = ioutil.WriteFile("dancypi/python/config.py", []byte(output), 0644)
	if err != nil {
			log.Printf("Error joining lines: %v", err)
	}
	if effect == 1 {
		cmd = exec.Command("python3", "dancypi/python/visualization.py", "scroll")
	} else if effect == 2 {
		cmd = exec.Command("python3", "dancypi/python/visualization.py", "energy")
	} else if effect == 3 {
		cmd = exec.Command("python3", "dancypi/python/visualization.py", "spectrum")
	} else if effect == 4 {
		cmd = exec.Command("python3", "dancypi/python/effect.py")
		log.Printf("Killed all display")
	}
	processes = append(processes, cmd)
	if err := cmd.Run(); err != nil {
		log.Printf("Ran process without problem\n")
	} else {
		log.Printf("error: %v", err)
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
