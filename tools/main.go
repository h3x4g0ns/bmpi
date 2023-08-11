package main

import (
  "fmt"
	"github.com/akamensky/argparse"
	"os"

  "bmpi/pkg/build"
  "bmpi/pkg/deploy"
  "bmpi/pkg/sim"
)

func main() {
  parser := argparse.NewParser("bmpi", "Program for bare metal pi builds")
  buildCmd := parser.NewCommand("build", "Builds application for pi")
  simCmd := parser.NewCommand("sim", "Tests application for pi")
  deployCmd := parser.NewCommand("deploy", "Deploys application to pi")
  err := parser.Parse(os.Args)
	if err != nil {
		fmt.Println(parser.Usage(err))
		return
	}

  switch {
  case buildCmd.Happened():
    build.Build()
  case simCmd.Happened():
    sim.Sim()
  case deployCmd.Happened():
    deploy.Deploy()
  default:
    fmt.Println(parser.Usage(err))
  }
}
