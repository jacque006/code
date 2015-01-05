// Example of a rot13 decoder in Go.
// Based on work done to complete http://tour.golang.org/methods/12 .

package main

import (
	"io"
	"os"
	"strings"
)

// Represents a valid range of byte values.
type byteRange struct {
	start byte
	end byte
}

// Base rot reader.
type rotReader struct {
	r io.Reader
	charRanges []byteRange
	increment byte
}

func RotReader(reader io.Reader, increment byte) rotReader {
	ranges := []byteRange{
		// A - Z
		byteRange{65, 90},
		// a - z
		byteRange{97, 122},
	}

    return rotReader{reader, ranges, increment}
}

// Retrieves a byteRange to use for incrementing the cyphered number.
// Will return the first valid range it finds, or an empty one if a
// valid range is not found.
func (reader rotReader) getRange(num byte) byteRange {
	ranges := reader.charRanges
	for i := range ranges {
		curRange := ranges[i]

		if num >= curRange.start && num <= curRange.end {
			return curRange
		}
	}

	return byteRange{}
}

// Increments the provided number to decipher it.
func (reader rotReader) IncrementWithinRange(number byte) byte {
	limitRange := reader.getRange(number)

	// Not a valid range? Return the original byte.
	if limitRange.start >= limitRange.end {
		return number
	}
	
	number += reader.increment
	
	// If we go over the end of the range, wrap around.
	if number > limitRange.end {
		over := number - limitRange.end
		number = limitRange.start - 1 + over
	}
	
	return number
}

func (reader rotReader) Read(b []byte) (n int, err error) {

	readBytes := make([]byte, 1)
	numRead, err := reader.r.Read(readBytes)
	
	if numRead < 1 || err == io.EOF {
		return n, err
	}
	
	for i := range readBytes {
		b[i] = reader.IncrementWithinRange(readBytes[i])
	}
	
	return numRead, nil
}

// Rot reader the deciphers 13 character shifts.
type rot13Reader struct {
	rotReader
}

func Rot13Reader(reader io.Reader) rot13Reader {
    return rot13Reader{RotReader(reader, 13)}
}

func main() {
	s := strings.NewReader("Lbh penpxrq gur pbqr!")
	r := Rot13Reader(s)
	io.Copy(os.Stdout, &r)
	// Output: You cracked the code!
}