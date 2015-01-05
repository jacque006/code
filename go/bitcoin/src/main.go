package main

import (
	"golang.org/x/net/websocket"
	"fmt"
	"log"
	"encoding/json"
)

type Transaction struct {
	hash string
	time int32
	inputs map[string]int64
	outputs map[string]int64
}

func SatoshisToBTC(value int64) float64 {
	return float64(value) / 100000000
}

func (t Transaction) String() string {
	s := ""
	s += fmt.Sprintf("Transaction Hash: %s\n", t.hash)
	s += fmt.Sprintf("Time: %v\n", t.time)
	s += " Inputs:\n"
	for key, value := range t.inputs {
		s += fmt.Sprintf("   %s : %v BTC\n", key, SatoshisToBTC(value))
	}
	s += " Outputs:\n"
	for key, value := range t.outputs {
		s += fmt.Sprintf("   %s : %v BTC\n", key, SatoshisToBTC(value))
	}
	s += "\n"
	return s
}

func TransactionFromJSON(b []byte) Transaction {	
	//fmt.Println(string(b))
	
	var objmap map[string]*json.RawMessage
	json.Unmarshal(b, &objmap)
	
	var x map[string]*json.RawMessage
	json.Unmarshal(*objmap["x"], &x)
	
	var hash string
	json.Unmarshal(*x["hash"], &hash)
	
	var time int32
	json.Unmarshal(*x["time"], &time)
	
	var out []*json.RawMessage
	json.Unmarshal(*x["out"], &out)
	
	outputMap := make(map[string]int64)
	for i := range out {
		var outMap map[string]*json.RawMessage
		json.Unmarshal(*out[i], &outMap)
	
		var addr string
		json.Unmarshal(*outMap["addr"], &addr)
		
		var value int64
		json.Unmarshal(*outMap["value"], &value)
		
		outputMap[addr] += value
	}
	
	var inputs []*json.RawMessage
	json.Unmarshal(*x["inputs"], &inputs)
	
	inputMap := make(map[string]int64)
	for i := range inputs {
		var inMap map[string]*json.RawMessage
		json.Unmarshal(*inputs[i], &inMap)
		
		var prev_out map[string]*json.RawMessage
		json.Unmarshal(*inMap["prev_out"], &prev_out)
		
		var addr string
		json.Unmarshal(*prev_out["addr"], &addr)
		
		var value int64
		json.Unmarshal(*prev_out["value"], &value)
		
		inputMap[addr] += value
	}
	
	return Transaction{hash, time, inputMap, outputMap} //, inputs, outputs}
}

func IsValidJson(b []byte) bool {

	var objmap map[string]*json.RawMessage
	err := json.Unmarshal(b, &objmap)
	
	return err == nil
}

func HandleTransaction(b []byte) {
	fmt.Println("Converting JSON to Transaction...")
	t := TransactionFromJSON(b)
	fmt.Println(t)
}

func main() {
	origin := "http://localhost/"
	url := "wss://ws.blockchain.info:443/inv"
	
	// Connect
	fmt.Printf("Connecting to %s...\n", url)
	ws, err := websocket.Dial(url, "", origin)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Connected!")

	// Subscribe
	subscriptionMessage := "{\"op\":\"unconfirmed_sub\"}";
	subscriptionBytes := []byte(subscriptionMessage)
	fmt.Printf("Subscribing with %s...\n", subscriptionMessage)
	if _, err := ws.Write(subscriptionBytes); err != nil {
		log.Fatal(err)
	}
	fmt.Println("Subscribed!")
	
	jsonData := make([]byte, 0)
	// Forever
	for {
		n := -1
		buffer := make([]byte, 1024)
		// Read
		fmt.Println("Reading from socket...")
		if n, err = ws.Read(buffer); err != nil {
			log.Fatal(err)
		}
		
		jsonData = append(jsonData, buffer[:n]...)
		
		if IsValidJson(jsonData) {
			// Process
			go HandleTransaction(jsonData)
			
			// Restart
			jsonData = make([]byte, 0)
		}
	}
}