# Superconducting Qubit Control Board

Custom FPGA-based control board for generating microwave I/Q signals used to drive superconducting qubits.

## Project Overview

This project is a hardware and FPGA control system for producing shaped control signals for superconducting qubit experiments. The board uses an FPGA to generate digital waveform data, a high-speed DAC to convert that data into analog I/Q signals, and an RF stage to upconvert the signals to microwave frequencies.

## Main Components

- FPGA digital control and waveform generation
- High-speed DAC for analog I/Q output
- TRF372017 RF modulator / PLL / VCO stage
- SPI control for configurable RF components
- Low-pass filtering between DAC and RF stages
- On-board power regulation and decoupling
- RF output through a controlled-impedance path to SMA

## Design Goals

- Generate programmable I/Q waveforms
- Support microwave signal generation for qubit control
- Keep the design modular and testable
- Document RF layout, DAC interfacing, FPGA control, and signal integrity design

## Repository Structure

SuperconductingQubitControlBoard/
- FPGA/ — Verilog, constraints, and Vivado files
- PCB/ — KiCad schematic, PCB layout, symbols, and footprints
- Docs/ — Notes, datasheets, and design references
- README.md

## Current Status

This project is currently in development. The main focus is schematic design, PCB layout, FPGA communication, and validating the signal chain from the FPGA to the RF output.
