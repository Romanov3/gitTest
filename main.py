from kivy.app import App
from kivy.uix.widget import Widget

# Window size
from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '270')

class MyGrid(Widget):
	username = 'hpfuser'
	password = ''
	csv_location = 'C:\\iuspt21ot_u4r.csv'
	save_in = 'C:\\ '
	host = "otqbh-cs.codm.gazprom.loc"
	port = 22
	opinion_csv = 0
	dirs = []

	def download_dir(self, remote_items, local_dir):
		import paramiko
		
		print('Connect to DNS:', self.dirs[int(self.opinion_csv)].split(';')[1])
		transport = paramiko.Transport((self.dirs[int(opinion_csv)].split(';')[1], self.port))
		transport.connect(username = self.username, password = self.password)
		sftp = paramiko.SFTPClient.from_transport(transport)
		
		errors = 0
		files = 0

		import os
		os.path.exists(local_dir) or os.makedirs(local_dir)
		print ('remote_items:', remote_items, 'local_dir:',local_dir)
		for remote_item in remote_items:
			local_path = local_dir + remote_item
			if os.path.isdir('/'.join( local_path.split('/')[:-1]) ):
				try:
					sftp.get(str(remote_item), local_path)
					files = files + 1
				except OSError:
					pass
					print ("This is not a file: ", remote_item)
					os.remove(local_path)
					errors = errors + 1
			else:
				try:
					sftp.stat(remote_item)
					os.makedirs('/'.join(local_path.split('/')[:-1]) )
					sftp.get(str(remote_item), local_path)
					files = files + 1
				except IOError:
					pass
					print ("No such file: ", remote_item)
					errors = errors + 1

		# Write log-file
		with open('log-file.txt', 'w') as logfile:
			num_copyfiles = "Number of copied files: " + str(files)
			num_error = "Number of errors: " + str(errors)
			logfile.write(num_copyfiles)
			logfile.write(num_error)

	def btt_show_csv_press(self, csv_location):
		self.csv_location = str(csv_location)

		try:
			with open(self.csv_location, 'r') as f:
				self.dirs = f.read().splitlines()
				print('dirs',self.dirs)
			# Clear window
			self.ids.textscr.text = ''
			#Show list: project, dns, module, file
			for i in range(0, len(self.dirs)):
				self.ids.textscr.text += str(i) + '   '
				self.ids.textscr.text += self.dirs[i] + '\n'
		except IOError:
			pass
			self.ids.textscr.text = 'File not found!'

	def btt_getalldata_press(self, username, password, save_in, opinion_csv):
		print('username:',username,
			"password:",password,
			'save_in', save_in,
			'opinion_csv ', opinion_csv)
		self.username = str(username)
		self.password = str(password)
		self.save_in = str(save_in)
		self.opinion_csv = int(opinion_csv)


		# Begin work server
		print('Option selected: ', int(opinion_csv))
		try:
			self.btt_show_csv_press(self.csv_location)
			print('Name of the project, server,module and file to the selected option',self.dirs[int(opinion_csv)].split(';'))
			self.download_dir(self.dirs[int(opinion_csv)].split(';'), self.save_in)
		except IndexError:
			pass
			self.ids.textscr.text = 'More then in csv!'
class MyApp(App):
	def build(self):
		return MyGrid()

if __name__ == '__main__':
	MyApp().run()