def pass2(object_file,SYMBTAB, listing_file,intermedfile,OPTAB, literal_table, directives,prog_name, prog_leng, start_add, LOCCTR):
     #open source file to read it
    def modify_add(address, indexed, object_code):

       z = str(address)[0]
       z = (indexed+bin(int(z, 16))[2:].zfill(3))
       z = hex(int(z, 2))[2:]
       object_code += (z+str(address)[1:])
       return object_code
    def write_to_text_record(object_file, text_record_length, text_record_object_code, text_record):
       text_record += (hex(int(text_record_length/2))[2:]+"^"+text_record_object_code)
       object_file.write("\n"+text_record)

    with   open(intermedfile, "r") as infile , open(listing_file,"w+") as outfile ,     open(object_file,"w+") as objectfile:

    #read  all input lines
     line = outfile.readlines()

    error_flag = 0
    text_record=""
    text_record_length=0
    end_exist = False
    objectfile.write("this is assembler code")
    for i , line in enumerate(line):
        j= False
        header_record = ""
        prog_name= line[8:16].strip()
        opcode  = line[15:21].strip()
        operand = line[22:41].strip() 
        lag= False
       
        directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW", "BASE", "LTORG"]

        if opcode != 'START' and i == 0:
               header_record +=('H'+prog_name+"000000"+hex(prog_leng)[2:])
               start_add = "000000"
               prog_leng = hex(line)[2:]
               #write header record to object program
               objectfile.write(header_record)
                      
               text_record = 'T'+"0"*2+line[i+1][0:5].strip()+"^"
               text_record = ""
        object_code = ""
        if opcode not in  directives:
            if opcode in OPTAB:
                object_code+=OPTAB[opcode] 
            elif line[14:15] == "="  :   
                 lag=True
                 if opcode in literal_table:
                            object_code = str(literal_table[0])
        if operand in SYMBTAB:
                add = SYMBTAB[operand]
                object_code = modify_add(add, "0", object_code)


        elif operand == "" and lag == False:
               object_code +="0000"

        elif ',X' in operand:
                #take first halfbyte from the operand
                operand = operand[:-2]
                add = SYMBTAB[operand]
                object_code = modify_add(add, "1", object_code)

        elif '=' in operand:
                operand = operand[1:]
                if operand in literal_table :
                    add = literal_table[operand][2]
                    object_code = modify_add(add, "0", object_code)

        elif lag == False:
                print(i)
                print("ERROR!, you are using a not correct symbol")
                error_flag += 1
       
                break

        #if opcode is a directive
        elif opcode == "BYTE":
            if operand[0] == 'X':
                object_code = operand[2:-1]     
            elif operand[0] == 'C':
                object_code = operand[2:-1].encode("utf-8").hex()
            object_code =object_code

        elif opcode == "WORD":
            object_code = hex(int(operand))[2:]
            blanks = 6-len(object_code)
            object_code = "0"*blanks+object_code

        blanks = 45-len(line)
        listing_file.write(line[:-1]+" "*blanks+object_code+"\n")

        discnt = False
        if opcode == "RESW" or opcode == "RESB":
            discnt = True
        
        if discnt and i+1 not in range(len(line)):
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            break
            

        
        if (discnt == True) and (line[i+1][15:21].strip()!='RESW' and line[i+1][15:21].strip()!='RESB'): 
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            text_record = 'T'+ '0'*2+line[i+1][0:5]+"^"
            text_record_length = 0
            text_record_object_code = ""           
        

        elif text_record_length + len(object_code) <=60 and discnt == False:
            text_record_object_code +=object_code+"^"
            text_record_length += len(object_code)
            
        elif discnt == False:
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            text_record = 'T'+ '0'*2+line[0:5]+"^"
            text_record_length = len(object_code)
            text_record_object_code = object_code+"^"
        
        if i+1 not in range(len(line)):
            write_to_text_record(object_file, text_record_length, text_record_object_code, text_record)
            

        #if the line is END line
        if opcode == "END":
            end_exist = True
        

    if end_exist == True:
        end_record = 'E'+start_add
        object_file.write("\n"+end_record)
    
      
        LOCCTR=hex(LOCCTR)[2:]
    
    

    if error_flag != 1:
        pl = str(prog_leng) 
        lc = str(LOCCTR) 
        
        print("name of the program: ",prog_name)
        print("length of the program: ",pl)
        print("LOCCTR: ",lc)
        print("symbol table : ",SYMBTAB)
        print("literal table : ",literal_table)
    
        SymbolTable = "\nSymbol"+" "*4+"address\n"
        for Symbol in SYMBTAB:
            blanks = 8-len(Symbol)
            SymbolTable += (Symbol+" "*blanks+"  "+ SYMBTAB[Symbol] + '\n')
    
        literalTable = "\nliteral"+" "*3+"value"+" "*9+"length"+" "*3+"address\n"
        for literal in literal_table:
            blanks = 10-len(str(literal))
            b = blanks*2
            literalTable += (literal+" "*blanks+ str(literal_table[literal][0])+" "*b+str(literal_table[literal][1])+" "*9+str(literal_table[literal][2]) + '\n')
    
                 
                   
pass2("object_file.obj","SYMBTAB", "listing_file.lst","intermed_file.mdt","OPTAB.txt", "literal_table", "directives","prog_name", "prog_leng", "start_add", "LOCCTR")
     