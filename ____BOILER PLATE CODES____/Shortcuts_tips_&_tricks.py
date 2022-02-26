
'''_________________SHORT CUTS, TIPS & TRICKS FOR: PYTHON, SUBLIME, REPL OR CMD_________________'''
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


___________________ SUBLIME __________________

	1) '''QUICKEST WAY TO MAKE A WORD-LIST IN SUBLIME'''
		1) copy and paste the list of words you found, e.g.:
						Industry Name
						Advertising
						Aerospace/Defense
						Air Transport
		2) press ctrl+A to select all
		3) press ctrl+shift+L to split selection into lines
		4) press ' or " or qoutate each row
		5) press ctrl+A to select all again (un-split the lines)
		6) press TAB to make an indent
		6) press ctrl+H and replace every TAB with ,
		7)throw in a couple of brackets and give it a name, and there you go!

	2) '''CONVERT SELECTION TO UPPERCASE OR LOWERCASE'''
		1) select the text
		2) press ctrl+K then ctrl+U
		3) press ctrl+K then ctrl+L

	3)'''MAKE SECTIONS STAY COLLAPSED WHEN OPENING SUBLIME'''
		1) https://github.com/titoBouzout/BufferScroll
		2) paste folder "BufferScroll" in Sublime packages folder
		3) path: '''r'C:\Users\Big Daddy B\AppData\Roaming\Sublime Text\Packages''''''''''																


___________________ PYTHON ___________________
	
	1) ....



____________________ REPL ____________________

	1) AUTOMATICALLY CLOSE THE PREVIOUS *REPL*[Python] WHEN REBUILDING?
		'''''''''''''''''''''''''''
		# From StackOverFlow.com #
			'''
			I did a dirty workaround which somehow works. I edited sublimerepl.py like:
				'''
				if view.name() == view_id:
			    found = view
			    old_rv = self.repl_view(found)
			    if old_rv:
			        old_rv.on_close()
			    window.focus_view(found)
			    break
			    '''
			Also I changed the on_close function from
			    '''
			 	self.repl.close()
			    '''
			to
			    '''
			 	self.repl.kill()
			    '''
			Now, the amount of Python instances stays the same.

			There are still some inconsistencies. When I use this code to talk to an Arduino, I'll get a PermissionError every other time. Adding time.sleep(1) didn't change this. I'm open to suggestions.

			EDIT: After using my "solution" for a while, I got annoyed by ***Repl Killed*** appearing everytime I executed code. Therefore, I decided to close the current REPL view and just start a new one. This way, I don't get an unnecessary amount of tabs, the background Python shell is closed and I start a fresh view every time I execute my code. The new code for sublimerepl.py is:
			    '''
				for view in window.views():
				    if view.name() == view_id:
				        view.close()
				        break
				view = window.new_file()
			    '''
			close() still has to be replaced by kill() for some reason.
		''''''''''''''''''''''''''''''



____________________ CMD _____________________

	1) ....

