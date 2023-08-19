package main

import (
  "fmt"
	"github.com/akamensky/argparse"
	"os"
)

func main() {
  parser := argparse.NewParser("bmpi", "Tool for bare metal pi builds")
  listCmd := parser.NewCommand("list", "Lists provisioned devices")
  err := parser.Parse(os.Args)
	if err != nil {
		fmt.Println(parser.Usage(err))
		return
	}

  switch {
  case listCmd.Happened():
    ListDevices()
  default:
    fmt.Println(parser.Usage(err))
  }
}
