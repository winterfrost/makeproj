import sys
import os
import shutil

file_handlers = {}
proj_name = "1"

def expose(rule, **kwargs):
	def wrapper(func):
		file_handlers[rule] = func
		return func
	return wrapper

def get_file_data(fname):
	ret = ""
	f = open(fname,'r')
	ret = f.read()
	f.close()
	return ret

def put_file_data(fname,data):
	f = open(fname,'w')
	f.write(data)
	f.close()

def replace_markers(txt):
	ret = txt
	marks = dict()
	marks["PROJ_NAME"] = proj_name
	
	for kw in marks:
		val = marks.get(kw)
		if not val:
			continue
		ret = ret.replace("{"+kw+"}",val)
	return ret

def default_handler(src,dst):
	data = get_file_data(src)
	data = replace_markers(data)
	put_file_data(dst,data)

@expose(os.path.join("vs","name.sln"))
def sln_hanlder(src,dst):
	dirpath = os.path.dirname(dst)
	path = os.path.join(dirpath,proj_name+".sln")
	default_handler(src,path)

@expose(os.path.join("vs","name.vcxproj"))
def vcxproj_handler(src,dst):
	dirpath = os.path.dirname(dst)
	path = os.path.join(dirpath,proj_name+".vcxproj")
	default_handler(src,path)

def generate_project():
		tpl_path = os.path.join(os.path.dirname(__file__),"tpl")
		proj_dir = os.path.join(os.getcwd(),proj_name)
		print "[~] full path: %s" % proj_dir
		if os.path.exists(proj_dir):
			shutil.rmtree(proj_dir)
		os.mkdir(proj_dir)
		
		for dirpath,dirs,files in os.walk(tpl_path):
			for f in files:
				full_path = os.path.join(dirpath,f)
				path = full_path.replace(tpl_path+"\\","")
				dst = os.path.join(proj_dir,path)
				
				dst_dir = os.path.dirname(dst)
				if not os.path.exists(dst_dir):
					os.makedirs(dst_dir)
				
				func = file_handlers.get(path)
				if not func:
					func = default_handler
				func(full_path,dst)

def main():
	global proj_name
	if len(sys.argv) < 2:
		print "Usage: makeproj.py <proj_name>"
		return 1
	proj_name = sys.argv[1]
	print "[+] project name: %s" % proj_name
	generate_project()
	return 0

main()

