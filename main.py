#!/usr/bin/env python3
"""
Launcher for FlipFinder_AI_GUI

Usage:
  python main.py run    # launches Streamlit app
  streamlit run app.py  # equivalent direct call
"""
import sys
import os


def print_usage():
	print("FlipFinder AI GUI")
	print("\nUsage:")
	print("  python main.py run    # launches the Streamlit app")
	print("  streamlit run app.py  # launch directly with Streamlit")


if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] in ("run", "start"):
		os.execvp("streamlit", ["streamlit", "run", "app.py"])
	else:
		print_usage()
