def pass1 (source_file , OPTAB1 , intermed_file):
  
  
  SYMBTAB = {}
  OPTAB = {}
  prog_name = ""
  prog_leng = 0
  start_add = 0
  error_flag = 0
  LABLE = ""
  OPCODE = ""
  OPERAND = 0
  COMMENT = ""
  with open (OPTAB1 , "r") as opcode_table:
     for line in opcode_table:
            opcode = line.strip().split()
           
            OPTAB[opcode[0]]=3
  

   
       
 # List of directives
  directives = ["START", "END", "BYTE", "WORD", "RESB", "RESW", "BASE", "LTORG"]
  
  with open (source_file, "r") as infile ,open (intermed_file , "w")as outfile : 
    line = infile.readline()

    if  line[9:15].strip()=="START":
            prog_name = line[0:8].strip()
            start_add = int (line[16:35],16)
            LOCCTR = start_add
            
           
    else: 
                LOCCTR = 0
    while line !="":

       
        line = line.strip()  # Remove leading/trailing whitespace
        parts = line.split()  # Split line into parts
 
 
  
          
        
       
        
       
        if parts[0] in OPTAB:
            OPCODE = parts[0]

        else :
            LABLE = parts[0]
            if len(parts) > 1:
               OPCODE = parts[1]     

           
            if  LABLE in SYMBTAB:
                error_flag = True
                print("Error: Duplicate symbol")
        
        if len(parts)>1 and parts[1] != 'END':  # Only add labels with instructions to SYMTAB
           
            SYMBTAB[LABLE] = LOCCTR
      
            outfile.write(f"{LOCCTR:04X}  {line}\n")
        

       
        #if found
            operand = line[16:35].strip()
            if OPCODE in OPTAB:
            #add 3 {instruction length}
               
                LOCCTR+=3
            elif OPCODE in directives:
                if OPCODE == "WORD":
                    LOCCTR += 3

            elif OPCODE == "RESW":
                    operand = line[16:35].strip()
                    LOCCTR += 3 * int(operand)

            elif OPCODE == "RESB":
                    operand = line[16:35].strip()
                    LOCCTR += int(operand)

            elif OPCODE == "BYTE":
                    operand = line[16:35].strip()
            #find the length of constant in bytes and add it to loc_ctr
            elif opcode == "LTORG":
                for literal in literal_table:
                    literal_table[literal][1] = hex(LOCCTR)[2:]
                    outfile.write(f"{LOCCTR:04X}  *       ={literal}\n")
                    LOCCTR += len(literal_table[literal][0]) // 2
                literal_table = {}
            else:
                error_flag = True
                print("Error: Invalid operation code")
                break
            
    

        else:
    #set error flag
            error_flag = 1
            print("invalid operation code" "," "Please enter valid operation code")
    
        if(OPCODE == "END"):
             if line[0:8] in infile== "":
               outfile.write("       "*6+line+"\n")
       
             
        line = infile.readline()  #reed lines from source file 
        
    #save (loc_ctr - starting add ) as program length
    prog_leng = int(LOCCTR) - int(start_add)

    print(prog_leng , prog_name)
    print(SYMBTAB)
    #close file
    infile.close()
    outfile.close()
    
    if error_flag != 1:
        import pass2 
        pass2.send_tables(SYMBTAB, OPTAB, literal_table, directives,prog_name, prog_leng, start_add, LOCCTR)

pass1("source_file.asm" , "OPTAB.txt" , "intermed_file.mdt") 