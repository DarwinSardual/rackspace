def filter_domains(input_file, output_file):
    domain_file = open(input_file, "r")
    domain_file_filtered = open(output_file, "a")
    
    domains = domain_file.readlines()
    
    for domain in domains:
        domain = domain.strip("\n")
        if not filter_int(domain):
            domain_file_filtered.write(domain + "\n")
            
    domain_file.close()
    domain_file_filtered.close()

def filter_int(s):
    
    try:
        int(s)
        return True
    except ValueError:
        return False
        
if __name__ == "__main__":
    filter_domains("domains_04_27_2018.txt",  "domains_04_27_2018_filtered.txt")
    print("Finish filtering")
