import math

#A horrible Python implementation of SHA-256

max_val = 2**32
def binprint(a):
	binary_formatted = format(a, 'b')
	binary_formatted = ('0' * (32 - len(binary_formatted))) + binary_formatted
	b = binary_formatted
	print(b[:8], b[8:16], b[16:24], b[24:32])

#Done!
def s0(a):
	return ((rot(a, 7) ^ rot(a, 18)) ^ (a >> 3)) % max_val
def s1(a):
	return (rot(a, 17) ^ rot(a, 19)) ^ (a >> 10) % max_val
def S0(a):
	return (rot(a, 2) ^ rot(a, 13)) ^ rot(a, 22) % max_val
def S1(a):
	return (rot(a, 6) ^ rot(a, 11)) ^ rot(a, 25) % max_val
def rot(a, unit):
	lower = a & (2**unit - 1)
	lower = lower << (32 - unit)
	a = a >> unit
	return a + lower

def ch(a, b, c):
	return ((a & b) + (~a & c)) % max_val
def maj(a, b, c):
	return (((a & b) ^ (a & c)) ^ (b & c)) % max_val

primes =  [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311]
def gen_constants():
	out = []
	for i in primes:
		cube_root = i**(1/3)
		cube_root = cube_root - math.floor(cube_root)
		cube_root = math.floor(cube_root * (2**32))
		out.append(cube_root)
	return out

def gen_constants_2():
	out = []
	for i in range(8):
		sqr = primes[i]**(1/2)
		sqr = sqr - math.floor(sqr)
		sqr = sqr * (2**32)
		sqr = math.floor(sqr)
		out.append(sqr)
	return out


constants = [1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298]
constants_2 = [1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225]

def sha(message):
	#generate blocks from data
	blocks = gen_blocks(message)

	#expand blocks
	for b in blocks:
		for i in range(16, 64):
			b.append((s1(b[i-2]) + b[i-7] + s0(b[i-15]) + b[i-16]) % max_val)

	#correct till here

	old_v = constants_2.copy()
	v = old_v.copy()
	for b in blocks:
		#for each block
		v = old_v.copy()
		for i in range(64):
			#for each word
			temp1 = (S1(v[4]) + ch(v[4], v[5], v[6]) + v[7] + constants[i] + b[i]) % max_val
			temp2 = (S0(v[0]) + maj(v[0], v[1], v[2])) % max_val
			for j in range(1,8):
				v[-j] = v[-j - 1]
			v[0] = (temp1 + temp2) % max_val
			v[4] = (v[4] + temp1) % max_val

		for t in range(8):
			v[t] = (v[t] + old_v[t]) % max_val
		old_v = v.copy()
	return v


#returns list of blocks which are lists of ints
def gen_blocks(message):
	data = bytearray(message, 'utf-8')
	data.append(128)
	block_count = (((len(data) * 8) + 65) // 512) + 1

	msg_int_arr = []
	offset = len(data) % 4
	for i in range(0, len(data) - (len(data) % 4), 4):
		msg_int_arr.append((data[i] << 24) + (data[i + 1] << 16) + (data[i + 2] << 8) + (data[i + 3]))

	if offset != 0:
		last_val = 0
		for j in range(offset):
			last_val += data[len(data) - offset  + j] << (24 - (8 * j))
		msg_int_arr.append(last_val)

	blocks = []
	for i in range(block_count):
		current_block = []
		for j in range(16):
			if i == block_count - 1 and j > 13:
				#append msg length and break
				msg_len = (len(data) - 1) * 8
				current_block.append(msg_len >> 32)
				current_block.append(2**32 if msg_len > 2**32 else msg_len)
				break
			if (i * 16) + j < len(msg_int_arr):
				#if message is still going
				current_block.append(msg_int_arr[(i * 16) + j])
			else:
				current_block.append(0)
		blocks.append(current_block)

	return blocks

if __name__ == "__main__":
	h = sha(input())
	out = ""
	for val in h:
		out = out + hex(val)[2:]
	out = ('0' * (64 - len(out))) + out
	print(out)