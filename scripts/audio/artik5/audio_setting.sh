#!/bin/sh

amixer sset "Digital Output Volume1 L (Manual Mode)" 120
amixer sset "Digital Output Volume1 R (Manual Mode)" 120
amixer sset "Mic Gain Control" 3
amixer sset "Mic Bias MUX" "IN1"
amixer sset "IN1 MUX" "Mic Bias"
amixer sset "Input Select MUX" "LIN1/RIN1"
amixer sset "ADC MUX1" "Mono"
amixer sset "MIC MUX" "AMIC"
amixer sset "ADCPF MUX" "ADC"
amixer sset "DACHP" "ON"
