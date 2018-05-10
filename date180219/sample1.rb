#!/usr/bin/ruby
#-*-coding:utf-8 -*-
#
#数独ソルバー(しらみつぶし法）by Satoshi Sato, 2014
#
def make_grid(string)
	#セル番号は, 0から80
	#各セルの値は,確定している場合は整数(1-9), 未確定の場合はnil
	string.split(//).collect{|c| c == "." ? nil : c.to_i}
end

def print_grid(grid, pad="\n")
	print (0..8).collect{|i|
		grid[9*i, 9].collect{|v| (v || '.')}.join('')}.join(pad), "\n"
end

def row (grid, p)	#行
	grid[9 * (p/9), 9]
end

def column (grid, p)	#列
	(0..8).collect{|k| grid[9*k+p%9]}
end

def square (grid, p)	#3×3の正方形
	(0..8).collect{|k| grid[9*(3*(p/9/3)+(k/3))+3*(p%9/3)+(k%3)]}
end

def empty_cells(grid)
	(0..80).select{|p| !grid[p]}
end

def possible_numbers (grid, p)
	(1..9).to_a - fixed_numbers(grid, p)
end

def fixed_numbers(grid, p)
	(row(grid, p).compact | column(grid, p).compact | square(grid, p).compact)
end

def solve(grid)
	pl = empty_cells(grid).collect{|p|
		[p, possible_numbers(grid, p)]}.sort_by{|x| x[1].length}
	if pl.empty?
		grid
	else
		p, number = pl[0]
		number.each do |v|
			grid[p] = v
			if solve(grid)
				return grid
			end
		end
		grid[p] = nil
		return false
	end
end

ARGF.each do |line|
	line.chomp!
	print_grid(solve(make_grid(line.gsub(/\s/, ''))))
end
