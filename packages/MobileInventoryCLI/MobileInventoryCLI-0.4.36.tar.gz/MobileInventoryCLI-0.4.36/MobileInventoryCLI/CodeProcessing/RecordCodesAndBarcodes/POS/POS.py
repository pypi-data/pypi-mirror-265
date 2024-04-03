import pandas as pd
import csv
from datetime import datetime
from pathlib import Path
from colored import Fore,Style,Back
from barcode import Code39,UPCA,EAN8,EAN13
import barcode,qrcode,os,sys,argparse
from datetime import datetime,timedelta,date
import zipfile,tarfile
import base64,json
from ast import literal_eval
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base as dbase
from sqlalchemy.ext.automap import automap_base
from pathlib import Path
import upcean
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExtractPkg.ExtractPkg2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup.Lookup import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DayLog.DayLogger import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ConvertCode.ConvertCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.setCode.setCode import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Locator.Locator import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ListMode2.ListMode2 import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.Tasks import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.ExportList.ExportListCurrent import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *


import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc

class POS:
	def __init__(self,engine,parent):
		self.engine=engine
		self.parent=parent
		cmd_color=Fore.light_yellow
		explanation_color=Fore.light_green

		self.helpText=f'''
{cmd_color}CMD{Style.reset}- {explanation_color}Explanation{Style.reset}
{cmd_color}new_b|newb|nb{Style.reset}- {explanation_color}create new business information{Style.reset}
{cmd_color}view_db|viewb|vdb{Style.reset}- {explanation_color}view DEFAULT business information{Style.reset}
{cmd_color}view_all_business|view_ab|vab{Style.reset}- {explanation_color}view ALL business information{Style.reset}
{cmd_color}remove_id{Style.reset}- {explanation_color}remove business information by id, or comma separated list of id's{Style.reset}
{cmd_color}setdefaultid|sdi{Style.reset}- {explanation_color}set default business, and all others are set to non-default{Style.reset}
{cmd_color}edit_business|eb{Style.reset}- {explanation_color}set default business, and all others are set to non-default{Style.reset}
{cmd_color}search_billing_text|sbt{Style.reset}- {explanation_color}search billing text fields{Style.reset}
'''
		print("under dev!")
		while True:
			try:
				def mkT(text,self):
					return text
				cmd=Prompt.__init2__(None,func=mkT,ptext="Do What",helpText=self.helpText,data=self)
				if cmd in [None,]:
					return
				if cmd.lower() in ['new_b','newb','nb']:
					self.mkBusiness()
				elif cmd.lower() in ['view_db','viewdb','vdb']:
					self.viewDefault()
				elif cmd.lower() in ['view_all_business','view_ab','vab']:
					self.viewAll()
				elif cmd.lower() in ['remove_id',]:
					self.removeId()
				elif cmd.lower() in ['edit_business','eb']:
					self.edit_business()
				elif cmd.lower() in ['setdefaultid','sdi']:
					self.setdefaultid()
				elif cmd.lower() in ['search_billing_text','sbt']:
					self.searchBillingText()

			except Exception as e:
				print(e)

	def searchBillingText(self):
		try:
			#print([{i.name:str(i.type)} for i in Billing.__table__.columns])
			textFields=[i.name for i in Billing.__table__.columns if str(i.type) == "VARCHAR"]
			#print(textFields)
			with Session(self.engine) as session:
				def mkT(text,self):
					return text
				searchText=Prompt.__init2__(None,func=mkT,ptext=f"Search Text?",helpText=f"searches {textFields} for your text",data=self)
				if searchText in [None,]:
					return
				query=session.query(Billing)
				f=[]
				for field in textFields:
					try:
						f.append(getattr(Billing,field).icontains(searchText))
					except Exception as e:
						print(e)
						continue
				query=query.filter(or_(*f))
				results=query.all()
				ct=len(results)
				for num,r in enumerate(results):
					msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {r}"
					print(msg)
		except Exception as e:
			print(e)


	def setdefaultid(self):
		print(f"{Fore.light_red}Setting Default Business!{Style.reset}")
		while True:
			try:
				with Session(self.engine) as session:
					results=session.query(Billing).all()
					ct=len(results)
					for num,r in enumerate(results):
						r.default=False
						if num%50==0:
							session.commit()
						msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {r}"
						print(msg)
					session.commit()
					while True:
						try:
							def mkint(text,self):
								try:
									if text == '':
										return 0
									return int(text)
								except Exception as e:
									print(e)
							which=Prompt.__init2__(None,func=mkint,ptext=f"Which Bussiness Would you like to set the default for?",helpText=f"use a integer between 0-{ct-1}",data=self)
							if which in [None,]:
								return
							results[which].default=True
							session.commit()
							session.flush()
							session.refresh(results[which])
							msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {results[which]}\n{Fore.light_magenta}Default Set!{Style.reset}"

							break
						except Exception as e:
							print(e)


				break
			except Exception as e:
				print(e)
		#start a while loop with exceptions forcing loop to continue
		#print businesses
		#ask for which business to set default on and set default
		#commit
		#return to menu


	def edit_business(self):
		print(f"{Fore.light_red}Editing a Business has begun!{Style.reset}")
		while True:
			try:
				with Session(self.engine) as session:
					results=session.query(Billing).all()
					ct=len(results)
					for num,r in enumerate(results):
						msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {r}"
						print(msg)
					while True:
						try:
							def mkint(text,self):
								try:
									if text == '':
										return 0
									return int(text)
								except Exception as e:
									print(e)
							which=Prompt.__init2__(None,func=mkint,ptext=f"Which Bussiness Would you like to edit?",helpText=f"use a integer between 0-{ct-1}",data=self)
							if which in [None,]:
								return

							patient=results[which]
							fields={i.name:i.type for i in Billing.__table__.columns}
							for i in fields:
								while True:
									def mkBool(text,self):
										try:
											if text in ['y','yes','true','True','1','t']:
												return True
											else:
												return False
										except Exception as e:
											print(e)
											return None

									while True:
										editField=Prompt.__init2__(None,func=mkBool,ptext=f"Edit {i}(Type:{str(fields[i])}|OLD:{getattr(patient,i)})",helpText="answer yes or no, default is No",data=self)
										if editField in [None,]:
											return
										if editField == False:
											break
										else:
											while True:
												try:
													def mkType(text,typeT):
														try:
															if str(typeT) == 'FLOAT':
																return float(eval(text))
															elif str(typeT) == 'INTEGER':
																return int(eval(text))
															elif str(typeT) == 'DATE':
																return datePickerF(None)
															elif str(typeT) == 'BOOLEAN':
																return mkBool(text,None)
															else:
																return str(text)
														except Exception as e:
															print(e)
													nvalue=Prompt.__init2__(None,func=mkType,ptext="Set New Value to?",helpText="New value for {i} with type {fields[i]}",data=fields[i])
													if nvalue in [None,]:
														break
													print(nvalue)
													setattr(results[which],i,nvalue)
													session.commit()
													session.flush()
													session.refresh(results[which])
													msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {results[which]}\n{Fore.light_magenta}Changed!{Style.reset}"
													break
												except Exception as e:
													print(e)
											break
									break



							session.commit()
							session.flush()
							session.refresh(results[which])
							msg=f"{Fore.light_green}{num}/{Fore.light_red}{ct}{Style.reset} -> {results[which]}\n{Fore.light_magenta}Default Set!{Style.reset}"
							break
						except Exception as e:
							print(e)


				break
			except Exception as e:
				print(e)
		#start a while loop with exceptions forcing loop to continue
		#print businesses
		#ask for which business
		#loop from fields and prompt to change or leave,
		#if change, prompt for new value
		#once edits are done and committed, ask if more are needed to be edited
		#if yes, stay in while loop,else break

	def removeId(self):
		with Session(self.engine) as session:
			def mkList(text,data):
				try:
					tmp=[]
					l=text.split(",")
					for i in l:
						try:
							tmp.append(int(i))
						except Exception as e:
							print(e)
					return tmp
				except Exception as e:
					print(e)
					return None
			ids=Prompt.__init2__(None,func=mkList,ptext="BillingId's to remove",helpText="BillingId or BillingId's separated by a comma",data=self)
			if ids in [None,]:
				return
			ct=len(ids)

			for num,i in enumerate(ids):
				result=session.query(Billing).filter(Billing.BillingId).first()
				if ct == 0:
					print(f"{Fore.light_red}No Results were found to be default!{Style.reset}")
				else:
					print(f"Deleting {Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {result}")
					session.delete(result)
					session.commit()
			print(f"{Fore.light_green}There are {Style.reset}{Fore.light_magenta}{ct}{Style.reset}{Fore.light_green} deletions!")		

	def viewDefault(self):
		with Session(self.engine) as session:
			result=session.query(Billing).filter(Billing.default==True).all()
			ct=len(result)
			if ct == 0:
				print(f"{Fore.light_red}No Results were found to be default!{Style.reset}")
			else:
				for num,r in enumerate(result):
					print(f"{Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {r}")
				print(f"{Fore.light_green}There are {Style.reset}{Fore.light_magenta}{ct}{Style.reset}{Fore.light_green} results!")

	def viewAll(self):
		with Session(self.engine) as session:
			result=session.query(Billing).all()
			ct=len(result)
			if ct == 0:
				print(f"{Fore.light_red}No Results were found!{Style.reset}")
			else:
				for num,r in enumerate(result):
					print(f"{Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {r}")
				print(f"{Fore.light_green}There are {Style.reset}{Fore.light_magenta}{ct}{Style.reset}{Fore.light_green} results!")

	def mkBusiness(self):
		while True:
			try:
				with Session(self.engine) as session:
					MAP={}
					for column in Billing.__table__.columns:
						if column.name in ['BillingId',]:
							continue
						def cmdMethod(text,typeT):
							try:
								if typeT == "FLOAT":
									if text == '':
										return 0
									return float(text)
								elif typeT == "INTEGER":
									if text == '':
										return 0
									return int(text)
								elif typeT == "BOOLEAN":
									if text in ['y','yes','true','t','1','']:
										return True
									else:
										return False
								elif typeT == "DATE":
									if text == '':
										return datePickerF(None)
									else:
										try:
											return date(datetime.strptime(text,TIMEFORMAT)).date()
										except Exception as e:
											return datePickerF(None)
								else:
									return str(text)
							except Exception as e:
								raise e
						while True:
							try:
								msgText=f"{column.name}({str(column.type)})"
								col=Prompt.__init2__(self,func=cmdMethod,ptext=msgText,helpText=f"add data to {column.name} field as {column.type}",data=str(column.type))
								if col in [None,]:
									break
								MAP[column.name]=col
								break
							except Exception as e:
								print(e,repr(e))
					new_billing=Billing(**MAP)
					session.add(new_billing)
					session.commit()
					session.flush()
					session.refresh(new_billing)
				break
			except Exception as e:
				print(e,f"{Fore.light_yellow}{Style.bold}...restarting!{Style.reset}")