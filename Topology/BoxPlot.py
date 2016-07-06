#!/usr/bin/python
"""This is the python code to read the text file and plot Box and wiskers plot"""
import argparse
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def plotBoxPlot(httpdatalist, sshdatalist):
	"""Plots the box and whiskers graph"""
        data_to_plot = []
	httpdatalist = map(int, httpdatalist)
	sshdatalist = map(int, sshdatalist)
	data_to_plot.append(httpdatalist)
	data_to_plot.append(sshdatalist)
	fig = plt.figure(figsize = (13,8))
	ax1 = plt.subplot2grid((4,4),(0,0), rowspan = 4, colspan = 2)
	ax2 = plt.subplot2grid((4,4),(0,2), rowspan = 2, colspan = 2)
	ax3 = plt.subplot2grid((4,4),(2,2), rowspan = 2, colspan = 2)

        ax1.set_xticklabels(['HTTP' , 'SSH'])
	ax1.get_xaxis().tick_bottom()
	ax1.get_yaxis().tick_left()	
	ax1.set_xlabel('Protocol')
	ax1.set_ylabel('Milliseconds')

        ax2.set_xticklabels(['HTTP'])
        ax2.get_xaxis().tick_bottom()
        ax2.get_yaxis().tick_left()
        ax2.set_xlabel('Protocol')
        ax2.set_ylabel('Milliseconds')
	ax2.set_ylim(910,940)

        ax3.set_xticklabels(['SSH'])
        ax3.get_xaxis().tick_bottom()
        ax3.get_yaxis().tick_left()
        ax3.set_xlabel('Protocol')
        ax3.set_ylabel('Milliseconds')
	ax3.set_ylim(3300,3500)

	bp = ax1.boxplot(data_to_plot)
	bp1 = ax2.boxplot(httpdatalist)
	bp2 = ax3.boxplot(sshdatalist)
	#plt.show() 	
	fig.savefig('BoxandWhiskers.jpg', bbox_inches='tight')

def ExtractDatafromFile(DataFile):
	"""Extracts the protocol run duration in milliseconds and returns it in a list """
	datalist = []
	for line in open(DataFile, 'r'):
    		if 'Client Protocol Run Duration in milliseconds' in line:
        		data = line.split()
			datalist.append(data[len(data)-1])
	return datalist

def main():
    """Check user input and start client."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--HTTP", help="Result file after running HTTP Measurements",required=True)
    parser.add_argument("-S","--SSH", help="Result file after running SSH Measurements", required=True)
    args = parser.parse_args()
    
    httpdatalist = ExtractDatafromFile(args.HTTP)
    
    sshdatalist = ExtractDatafromFile(args.SSH)
    for data in httpdatalist:
    	print("http measurements "+str(data)+ " ms")

    for data in sshdatalist:
	print("ssh measurements " + str(data)+ " ms")

    plotBoxPlot(httpdatalist, sshdatalist)

if __name__ == "__main__":
    main()
