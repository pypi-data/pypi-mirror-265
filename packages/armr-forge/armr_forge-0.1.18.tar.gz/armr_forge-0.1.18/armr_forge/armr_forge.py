import json
from cryptography.fernet import Fernet
from datetime import date, timedelta
import pandas as pd
import numpy as np
import os
import time
import zipfile
import tarfile
import io
import tempfile
import bcrypt
import shutil
import sys
import base64
from multiprocessing import Pool

if __name__ == "__main__":
    print("This Module Cannot be run as script")
    sys.exit(0)

class forge:

    def __init__(self):
        self.name = "armr"
        self.state="closed"
        self.temp_path = None
        self.files = None
        self.session = None
        self.map=None


    # forge armr creates an empty armr file and specifies the map parameters
    def forge_armr(self,admin_username,admin_password,filepath,keypath,map_params):
        
        """
        Creates a portable encrypted blob storage system using tar.gz format.

        This method initializes a new encrypted storage system by generating master and admin keys,
        creating an admin user, and setting up an empty data structure ('map') for the storage of
        objects and features. It also creates an empty user data file and an empty change log file.
        All of these components are then bundled into a tar.gz archive for portability. This format
        allows for quick decompression and is suitable for further compression into more compact
        formats like tar.xz if desired.

        Parameters:
        - admin_username (str): The username for the admin account.
        - admin_password (str): The password for the admin account.
        - filepath (str): The file path where the tar.gz archive will be saved.
        - keypath (str): The file path where the admin key will be saved.
        - map_params (list of str): A list of parameter names to initialize the map data structure.

        Note:
        - The 'bcrypt' library is used for hashing admin credentials.
        - The 'cryptography.fernet' module is used for key generation and encryption.
        - The 'tarfile' module and 'io.BytesIO' class are used for creating the tar.gz archive.
        - It is assumed that this function is to be run in a secure environment as it prints out
        sensitive information to the console for confirmation purposes.

        Usage:
        - To create a new ARMR encrypted storage, call:
        `forge_armr(admin_username=<admin_username>, admin_password=<admin_password>,
        filepath=<archive_path>, keypath=<key_path>, map_params=<map_parameters_list>)`
        Ensure the storage and keys are handled securely after creation.
        """
        
        master_key = Fernet.generate_key()
        admin_key = Fernet.generate_key()
        user_encrypted_master_key = Fernet(admin_key).encrypt(master_key).decode("utf-8")

        # create admin key and login
        hashed_username = bcrypt.hashpw(admin_username.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        admin = {"user_name": hashed_username,"password":hashed_password,"key":user_encrypted_master_key,"policy":"admin"}
        print(admin)
        admin = Fernet(admin_key).encrypt(json.dumps(admin).encode("utf-8"))+ b"\n"
        

        
        # initialize an empty encrypted map json object
        mapdata = {"objects":0,"features":{"%ADDED%":{},"%TYPE%":{}}}
        for map_param in map_params:
            mapdata["features"][map_param]={}
            
        mapdata = Fernet(master_key).encrypt(json.dumps(mapdata,indent=3).encode("utf-8"))
    
        # initializa an empty byte stream to create an empty database, user list and change log
        empty = b""
    
        # match the data to the filenames
        tarfiles={"map_data.ejn":mapdata,"user_data.ejn":admin,"admin_user_data.ejn":empty,"objects.case":empty,"change_log.case":empty}
        
        # save the key to the same directory as the tar file
        print(keypath)
        with open(keypath,"wb") as keyfile:
            keyfile.write(admin_key)
    
        # write the files as bytes to the tar file using the buffer
        with tarfile.open(filepath, "w") as tar:
            # Add the file-like object to the tar, providing the TarInfo object for metadata
            for key in list(tarfiles.keys()):
                fileobject = io.BytesIO(tarfiles[key])
                tar_info = tarfile.TarInfo(name=key)
                tar_info.size = len(fileobject.getvalue())
                tar.addfile(tar_info, fileobject)
    
    # user_session holds the users credentials in order to validate key functions and deal with the encryption ad permissions
    def user_session(self,username,password,user_managed_key_path):
        """
        Establishes a user session by storing the user's credentials and key path.

        This method saves the provided username, password, and the path to the user-managed key
        in the current instance's session dictionary. It is a setup function that should be called
        at the beginning of a user's session to ensure that subsequent actions can be authenticated
        and authorized appropriately.

        Parameters:
        - username (str): The username of the user.
        - password (str): The password of the user.
        - user_managed_key_path (str): The filesystem path to the user's managed key.

        Usage:
        - To start a user session, call:
        `user_session(username=<username>, password=<password>, user_managed_key_path=<key_path>)`
        This should be done before the user attempts to perform any actions that require authentication.
        """
        self.session={"username":username,"password":password,"user_managed_key_path":user_managed_key_path}
    
    # validate user logs in the user and decrypts the master key for that user returning a policy and master key
    def validate_user(self):
        """
        Validates the user's credentials against the stored user data.

        This method attempts to validate the current user by checking the provided username and password
        against the encrypted records in the user data file. It reads the user-managed key from the path
        specified in the current session, decrypts the user records, and then compares the encrypted
        username and password to validate the session. If validation is successful, it returns a dictionary
        with the user's name, policy, and master key; otherwise, it raises a ValueError.

        Returns:
        dict: A dictionary containing the user's name, policy, and decrypted master key if validation is successful.

        Raises:
        ValueError: If validation fails at any point.

        Usage:
        - To validate a user, ensure `user_session` is called first, and then call:
        `validate_user()`
        The function will access the session information and proceed with validation.

        Notes:
        - The method assumes that `self.session` has been appropriately set with 'username',
        'password', and 'user_managed_key_path' before this method is called.
        - The user data file should be in the 'user_data' path of `self.files`.
        - User records are expected to be encrypted in the user data file.
        - Passwords and usernames are expected to be stored as bcrypt hashes.
        """
        username = self.session["username"]
        password =  self.session["password"]
        user_key_path = self.session["user_managed_key_path"]

        try:
            with open(user_key_path, "rb") as keyfile:
                user_key = keyfile.read()
        except Exception as e:
            print(f"Failed to read user key")
            return None

        try:
            with open(self.files["user_data"], "rb") as udata:
                for line in udata:
                    try:
                        user_record = line
                        decrypted_user_record = json.loads(Fernet(user_key).decrypt(user_record).decode("utf-8"))
                        user_validated = bcrypt.checkpw(username.encode("utf-8"), decrypted_user_record["user_name"].encode("utf-8"))
                        password_validated = bcrypt.checkpw(password.encode("utf-8"), decrypted_user_record["password"].encode("utf-8"))
                        if user_validated and password_validated:
                            return {"user":username,"policy":decrypted_user_record["policy"],"master":Fernet(user_key).decrypt(decrypted_user_record["key"].encode("utf-8"))}
                        else:
                            print(f"Validation failed for user")
                    except json.JSONDecodeError:
                        print(f"decoding failed for line")
                    except:
                        #check next line
                        pass
        except FileNotFoundError:
            print(f"User data file not found")
        except Exception as e:
            print(f"Failed to validate user")

        raise ValueError("failed to validate")
    
    # loads the map into memory after validating the user
    def load_map(self):
        """
        Loads and decrypts the map data using the master key obtained from the validated user.

        This method reads the encrypted map data from the file specified in `self.files["map"]`. It then
        attempts to decrypt this data using the master key retrieved from the validated user's details.
        If the decryption and the subsequent JSON parsing are successful, it returns the map data as a dictionary.

        Returns:
        dict: The decrypted and parsed map data.

        Raises:
        ValueError: If the user validation fails or the map data cannot be decrypted and parsed.

        Usage:
        - To load the map, call `load_map()` after the user session has been established.
        The function will read the map file path from `self.files["map"]`, validate the user,
        and then decrypt and parse the map data.

        Notes:
        - This method depends on the successful validation of the user, which should be ensured
        by having called `validate_user` implicitly or explicitly before this method.
        - The method assumes that the map data is stored in JSON format and is encrypted.
        """
        with open(self.files["map"],"rb") as mapfile:
           mapdata =  mapfile.read()
        try:
            map = Fernet(self.validate_user()["master"]).decrypt(mapdata).decode("utf-8")
            map = json.loads(map)
        except:
            raise ValueError("failed to validate user and load map")
        return map
    
    # opend the armr file, validates the user, and loads the map
    def open_armr(self,tcase_filepath):
        """
        Extracts the contents of an ARMR (Advanced Records Management Resource) tar file to a temporary directory
        and loads the map by validating the user session.

        This method is responsible for opening an ARMR file, which is a tarball containing the essential files
        for the operation of a record management system. These files include the objects, map, user data, change log,
        and admin user data. The method extracts these files to a temporary directory, sets the file paths in the 
        instance, validates the user session, and loads the map data into memory.

        Parameters:
        tcase_filepath (str): The file path to the ARMR tar file to be opened.

        Exceptions:
        Exception: General exception is caught and printed, and if an exception occurs, the temporary directory
                is cleaned up to prevent residual files from remaining.

        Usage:
        - Call `open_armr()` with the file path to the ARMR tar file after initiating the class instance.
        The method will extract the files and attempt to validate the user session and load the map data.

        Notes:
        - This method assumes that the ARMR file follows a specific structure and naming convention for the contained files.
        - It also assumes that the user session has already been established to facilitate the loading of the map data.
        - In the event of an exception, the method attempts to clean up any temporary directories created during its process.
        """
        print("Opening ARMR Please Wait...")
        try:
            self.temp_path = tempfile.mkdtemp(prefix='ARMR', suffix='_tmp', dir='./')
            with tarfile.open(tcase_filepath, "r") as tar:
                tar.extractall(path=self.temp_path)
            self.files = {
                "objects":self.temp_path+"\\objects.case", \
                "map":self.temp_path+"\\map_data.ejn", \
                "user_data":self.temp_path+"\\user_data.ejn", \
                "change_log":self.temp_path+"\\change_log.case", \
                "admin_user_data":self.temp_path+"\\admin_user_data.ejn" \
            }
            print("Validating User Session and Loading Map")
            self.map = self.load_map()
        except Exception as e:
            print(e)
            if self.temp_path is not None:
                shutil.rmtree(self.temp_path)
        self.state="open"
        print("Opened Successfully")
    
    # saves the armr file and deletes the temp folder
    def close_armr(self,tcase_filepath):
        """
        Archives the contents of the temporary directory created for an ARMR session into a tar file and then
        cleans up the temporary directory.

        This method is the complement to `open_armr()`. It takes the contents that have been possibly modified
        during the session and re-archives them into the original tar file specified by the `tcase_filepath`.
        It then removes the temporary directory used during the session to ensure no temporary files are left on the disk.

        Parameters:
        - tcase_filepath (str): The file path where the tar file will be saved.

        Side Effects:
        - Creates or overwrites a tar file at the given file path.
        - Deletes the temporary directory used during the ARMR session.

        Usage:
        - After completing all necessary operations with the opened ARMR, call `close_armr()` with the path
        to save the tar file. This will archive the files and clean up the temporary directory.

        Notes:
        - It is critical to call this method before ending the session to ensure that all changes are saved
        and the temporary files are not left behind.
        - This method sets `self.temp_path` to None after successful closure to signify that the session is closed.
        - The method assumes that `self.temp_path` is correctly set during the session and will be non-null
        when calling this method.
        """
        print("Closing ARMR Please Wait...")
        if self.state=="open":
            with tarfile.open(tcase_filepath, "w") as tar:
                for root, dirs, files in os.walk(self.temp_path):
                    for file in files:
                        fullpath = os.path.join(root, file)
                        tar.add(fullpath, arcname=os.path.relpath(fullpath, self.temp_path))
                shutil.rmtree(self.temp_path)
                self.temp_path=None 
                self.state="closed"
            print("Closed Successfully")
        else:
            print("ARMR is Closed")
    
    # creates a new user, appends them to users and admin records and then saves their unique key
    def new_user(self,username,password,policy_name,new_key_path):
        admin_username = self.session["username"]
        admin_password =  self.session["password"]
        admin_key_path = self.session["user_managed_key_path"]
        """
        Creates a new user with encrypted credentials and policies.

        This method takes a username, password, and policy name, then generates encrypted user credentials
        and policy details. It creates a user-managed access key for the new user and uses it to encrypt
        and obfuscate user data. Additionally, it encrypts a separate record of the user that can be managed
        by an admin user with the appropriate permissions.

        Parameters:
        - username (str): The username for the new user.
        - password (str): The password for the new user.
        - policy_name (str): The policy name associated with the new user's account.
        - new_key_path (str): The file path where the new user's key will be stored.

        Returns:
        - str: A confirmation message indicating that the user has been created.

        Raises:
        - ValueError: If the session policy is not 'admin', indicating that the current user does
                    not have the necessary administrative privileges to create a new user.

        Note:
        - The method assumes the existence of a 'validate_user' method that checks the current
        user's credentials and returns their access policy among other data.
        - It also assumes the 'session' attribute to contain the current admin user's credentials
        and key path for validation purposes.
        - The 'files' attribute should contain the keys 'user_data' and 'admin_user_data' with
        paths to the files where user records are stored.
        - The bcrypt library is used for hashing credentials.

        Usage:
        - To create a new user, call:
        `new_user(username=<username>, password=<password>, policy_name=<policy_name>, new_key_path=<path_to_user_key>)`
        Ensure you have admin privileges before invoking this method.
        """
        # decrypt the master_key by validating the admin
        with open(admin_key_path,"rb") as mkey:
            admin_key = mkey.read()

            
            dict_data = self.validate_user()
            master_key = dict_data["master"]
            policy = dict_data["policy"]
            
            if policy!="admin":
                raise ValueError("This Function Requires Admin Permissions")
                
        # Generate the hashed username and password
        hashed_username = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
    
        # generate a user key and use it to encrypt the master_key
        new_user_key = Fernet.generate_key()
        user_encrypted_master_key = Fernet(new_user_key).encrypt(master_key).decode("utf-8")
    
        # create a user data jsonl line and encrypt it with the new user's key
        user_record = {"user_name": hashed_username,"password":hashed_password,"key":user_encrypted_master_key,"policy":policy_name}
        user_record = Fernet(new_user_key).encrypt(json.dumps(user_record).encode("utf-8"))+ b"\n"
    
        # create a user data jsonl to be encrypted by the master key and managed by the admin
        admin_record = {"user_name": username,"user_key":new_user_key.decode("utf-8"),"user_master_key":user_encrypted_master_key}
        admin_record = Fernet(admin_key).encrypt(json.dumps(admin_record).encode("utf-8"))+ b"\n"

        with open(new_key_path,"wb") as nkey:
            nkey.write(new_user_key)

        with open(self.files["user_data"],"ab") as ufile:
            ufile.write(user_record)
        
        with open(self.files["admin_user_data"],"ab") as aufile:
            aufile.write(admin_record)

        return "User Created"
    
    # lists the users, usernames, and keys to allow the admin to perform user management
    def list_users(self):
        """
        Retrieves and decrypts a list of all user data.

        This method opens and reads an encrypted file containing user data. It decrypts the file
        contents using a Fernet symmetric encryption key obtained from the user's managed key file.
        It requires that the user invoking this method has admin privileges as determined by the
        policy information in the user's validation data.

        Returns:
        - userlist (list of dict): A list of dictionaries, where each dictionary contains the
                                decrypted data of a single user.

        Raises:
        - ValueError: If the policy of the user is not 'admin', indicating that the user does
                    not have administrative privileges required to list users.
        - FileNotFoundError: If the file paths for 'admin_user_data' or 'user_managed_key_path'
                            in the 'files' or 'session' attributes do not exist.
        - KeyError: If required keys are not found in 'files', 'session', or the dictionary
                    returned by 'validate_user'.
        
        Note:
        - The function assumes the existence of a 'validate_user' method that returns a
        dictionary containing at least a 'policy' key to check for admin privileges.
        - It also assumes that the 'files' and 'session' attributes contain the keys
        'admin_user_data' and 'user_managed_key_path', respectively, with paths to the
        relevant files.
        
        Usage:
        - To list all users, simply call:
        `list_users()`
        Make sure that the user has admin privileges before calling.
        """
        with open(self.files["admin_user_data"],"rb") as users:
            with open(self.session["user_managed_key_path"],"rb") as keyfile:
                key = keyfile.read()
                suite = Fernet(key)
                dict_data = self.validate_user()
                policy = dict_data["policy"]
                if policy!="admin":
                    raise ValueError("This Function Requires Admin Permissions")

                userlist = [json.loads(suite.decrypt(user).decode("utf-8")) for user in users]
                return userlist
    
    # archives a file or folder at the given path and saves it to the io buffer as a byte stream
    def zip_path_to_bytes(self,file_or_folder_path):
        """Zip the contents of a folder or a single file and return the zip file's bytes.

        Args:
        - file_or_folder_path (str): The path of the folder or file to zip.

        Returns:
        - bytes: The bytes of the zip file.
        """
        # Create a byte stream to hold the zip file's bytes
        zip_buffer = io.BytesIO()

        # Initialize the zipfile object with the byte stream
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # If the path is a directory, zip its contents
            if os.path.isdir(file_or_folder_path):
                # The root directory within the ZIP file
                root_len = len(os.path.dirname(os.path.abspath(file_or_folder_path)))

                # Iterate over all the files in the directory
                for root, dirs, files in os.walk(file_or_folder_path):
                    archive_root = os.path.abspath(root)[root_len:].strip(os.sep)
                    # Add all files in this directory to the ZIP file
                    for file in files:
                        full_path = os.path.join(root, file)
                        archive_name = os.path.join(archive_root, file)
                        zipf.write(full_path, archive_name)
            # If the path is a file, zip that file
            elif os.path.isfile(file_or_folder_path):
                # Add the file to the ZIP file
                zipf.write(file_or_folder_path, os.path.basename(file_or_folder_path))
            else:
                raise FileNotFoundError("The specified path does not exist")

        # Make sure the buffer's pointer is at the start
        zip_buffer.seek(0)

        # Get the bytes of the zip file
        return zip_buffer.getvalue()
    
    # transforms datatypes to the correct dictionary format for appending
    def smelt(self,smelt_object,data_type):
        """
        Processes an input object by transforming it into a list of dictionaries with stringified values.

        The method is designed to handle two types of input: a DataFrame and an archive. If the input is a DataFrame,
        it checks for the presence of all indexed features and converts each row into a dictionary, assigning a unique
        ID, addition date, version number, and type 'RECORD'. For an archive, it zips the specified file path, encodes
        it into base64, and creates a dictionary with the provided index information, assigning a unique ID, addition
        date, version number, and type 'ARCHIVE'.

        Parameters:
        - smelt_object: The input object to process. This is expected to be a DataFrame when `data_type` is 'dataframe'
                        and a dictionary with 'index' and 'filepath' keys when `data_type` is 'archive'.
        - data_type (str): The type of the `smelt_object`. Supported types are 'dataframe' and 'archive'.

        Returns:
        - dict_list (list of dict): A list of dictionaries representing the processed records, each with a unique '%ID%'
                                    key, '%ADDED%' date, '%VERSION%' number, and '%TYPE%' indicating the record type.

        Raises:
        - KeyError: If any expected features are missing from the `smelt_object` based on the 'features' key in the
                    application's map.

        Note:
        - The method assumes that 'self.map' is a dictionary containing a key 'objects' that indicates the current count
        of objects, which is used to assign IDs to new records.
        - The method also assumes that 'self.map["features"]' contains the keys of features that are expected to be
        present in the input `smelt_object`.
        - For 'archive' type, the 'index' should contain metadata and 'filepath' should indicate the file to be archived.

        Usage:
        - To process a DataFrame and transform it into a list of dictionaries, call:
        `smelt(smelt_object=<DataFrame>, data_type='dataframe')`
        - To process a file path and create an archive record, call:
        `smelt(smelt_object=<dict_with_index_and_filepath>, data_type='archive')`
        """
        dict_list = []
        start_id = self.map["objects"]
        
        if data_type=="dataframe":

            # check the indexed features are avialable in the incoming dataframe
            for feature in list(self.map["features"].keys()):
                if feature not in ["%ADDED%","%TYPE%"]:
                    if feature not in list(smelt_object.columns):
                        raise KeyError(f"missing: {feature} in data frame")
                
            # transform the dataframe into binary jsonl
            for i in smelt_object.index:
                record = dict(smelt_object.iloc[i])
                record["%ID%"]=start_id
                record["%ADDED%"] = str(date.today())
                record["%VERSION%"]=str(0)
                record["%TYPE%"]="RECORD"
                start_id +=1
                for key in list(record.keys()):
                    record[key]= str(record[key])
                dict_list.append(record)

        if data_type =="archive":
            # check the indexed features are avialable in the incoming dataframe
            for feature in list(self.map["features"].keys()):
                if feature not in ["%ADDED%","%TYPE%"]:
                    if feature not in list(smelt_object["index"].keys()):
                        raise KeyError(f"missing: {feature} in data archive index")
                
            archive_bytes = base64.b64encode(self.zip_path_to_bytes(smelt_object["filepath"])).decode('ascii')
            #archive_bytes = self.zip_path_to_bytes(smelt_object["filepath"])

            record = {}
            for key in list(smelt_object["index"].keys()):
                record[key]=smelt_object["index"][key]
            record["%BYTES%"]=archive_bytes
            record["%FROM_PATH%"] = smelt_object["filepath"]
            record["%ID%"]=start_id
            record["%ADDED%"] = str(date.today())
            record["%VERSION%"]=str(0)
            record["%TYPE%"]="ARCHIVE"
            dict_list.append(record)

        return dict_list
    
    # smelts and applies the objects to the objects file
    def append_objects(self,append_object,data_type):
        """
        Appends encrypted objects to a file and updates the mapping of features to object IDs.

        This function processes input data according to the specified data type using the 'smelt' method,
        encrypts the processed data, and appends it to a designated file. It additionally updates an index
        mapping unique feature values to their corresponding object IDs and increments the total object count.

        Parameters:
        - append_object (list/dict): The list of objects or a single object to be appended. If 'data_type' is
                                    'dataframe', this should be a DataFrame. If 'data_type' is 'archive', this
                                    should be a dictionary with the required structure for archiving.
        - data_type (str): The type of data being processed. This is used within the 'smelt' method to properly
                        process the `append_object`. Expected values are 'dataframe' or 'archive'.

        Operations:
        - For each object, the method encrypts the data using Fernet symmetric encryption with a key obtained
        from the user's master credentials.
        - The index of features to object IDs is updated with the new IDs.
        - The 'map' file is updated with the new object count and feature indices as encrypted JSON.

        Note:
        - This function assumes the existence of a 'smelt' method to process the input data and a 'validate_user'
        method to provide encryption keys.
        - The 'files' attribute must contain 'objects' and 'map' keys with paths to the respective files.
        - The 'map' attribute must contain a 'features' key that stores the feature-to-ID mapping and an 'objects'
        key for the total object count.
        - If 'data_type' is 'archive', the 'append_object' must include 'index' metadata and 'filepath' for the
        archive source.

        Raises:
        - KeyError: If essential keys are missing in the provided data or the application's 'map'.
        - FileNotFoundError: If the file paths specified in 'self.files' do not exist or are inaccessible.
        - Exception: Any exception raised by the 'smelt' method or during file operations is propagated.

        Usage:
        - To append a single object or a list of objects with the given data type, call:
        `append_objects(append_object=<object or list of objects>, data_type=<data type>)`
        - Example for a DataFrame:
        `append_objects(append_object=dataframe, data_type='dataframe')`
        - Example for an archive:
        `append_objects(append_object={'index': index_data, 'filepath': '/path/to/archive'}, data_type='archive')`
        """
        data = self.smelt(append_object,data_type)
        index_keys = list(self.map["features"].keys())
        map_data = self.map
        suite = Fernet(self.validate_user()["master"])
        with open(self.files["objects"],"ab") as file:
            for line in data:
                for key in index_keys:
                    try:
                        # try adding the id indice to the unique value for the feature in the index_keys
                        map_data["features"][key][line[key]].append(int(line["%ID%"]))
                    except KeyError:
                        map_data["features"][key][line[key]]=[]
                        map_data["features"][key][line[key]].append(int(line["%ID%"]))

                map_data["objects"]+=1
                encrypted_line=suite.encrypt(json.dumps(line).encode("utf-8"))+ b"\n"
                #print(encrypted_line)
                file.write(encrypted_line)

        with open(self.files["map"],"wb") as file:
            newmap = suite.encrypt(json.dumps(map_data).encode("utf-8"))
            file.write(newmap)
            
        self.map = map_data
    
    # retrieves specefied indices as dictionaries in a list
    def retrieve_slice(self,min_indice,max_indice):
        """
        Retrieves a slice of records from an encrypted file within the specified index range.

        This method decrypts and reads a range of records from a file, returning a list of 
        records that fall between the specified minimum and maximum indices. If the `max_indice`
        is `None`, the method retrieves all records starting from the `min_indice` up to the last
        record.

        Parameters:
        - min_indice (int): The minimum index from which to start retrieving records. Inclusive.
        - max_indice (int or None): The maximum index at which to stop retrieving records. Exclusive.
        If `None`, retrieval continues until the end of the file.

        Returns:
        - collection (list): A list of decrypted records (dictionaries) that fall within the specified
        index range.

        Raises:
        - ValueError: If `min_indice` is not an integer or if `max_indice` is neither `None` nor an integer.
        - KeyError: If the 'master' key is not found in the user's validation data or 'objects' key is not
        found in the map.
        - FileNotFoundError: If the file at `self.files["objects"]` does not exist.
        - json.JSONDecodeError: If a decrypted line cannot be parsed as JSON.

        Usage:
        - To retrieve records starting from index 10 to 20, call:
        `retrieve_slice(min_indice=10, max_indice=20)`
        - To retrieve all records starting from index 10 to the end of the file, call:
        `retrieve_slice(min_indice=10, max_indice=None)`

        Notes:
        - This method assumes that the records are stored in an encrypted format, with one record per line,
        in the file located at `self.files["objects"]`.
        - The user must be validated (and thus the 'master' encryption key must be available) before calling 
        this method.
        - The method assumes that `self.map` has been loaded and contains a valid count of objects at `self.map["objects"]`.
        """
        collection = []
        suite = Fernet(self.validate_user()["master"])
        with open(self.files["objects"],"rb") as file:
            if max_indice==None:
                max_ind = int(self.map["objects"])
            else:
                max_ind = max_indice
            indice=0
            for line in file:
                if (indice>=min_indice) & (indice<max_ind):
                    record = json.loads(suite.decrypt(line).decode("utf-8"))
                    for key in list(record.keys()):
                        if key== "%BYTES%":
                            record["%BYTES%"]="Byte_Stream"

                    collection.append(record)
                indice+=1
        return collection
    
    # returns the indices where the query is true for all queries
    def query_map(self,query_dictionary_list):
        """
        Executes a query against the feature map to retrieve intersecting indices.

        This method processes a list of query dictionaries, each specifying key-value pairs.
        It retrieves the indices associated with each value for the corresponding key from the map.
        Then, it intersects these indices across all queries to find common records that match all criteria.

        Parameters:
        - query_dictionary_list (list of dict): A list of dictionaries, where each dictionary contains
        key-value pairs representing the field to be queried and the value to be matched in that field.

        Returns:
        - current (list): A sorted list of indices that represent the intersection of all query results.
        If the queries result in no intersection, an empty list is returned.

        Raises:
        - KeyError: If any value from the query is not found in the corresponding field within the map,
        or if a key (field) does not exist.

        Usage:
        - To perform a query to find records where the field 'category' has the value 'books' and the
        field 'author' has the value 'Smith', call:
        `query_map([{'category': 'books', 'author': 'Smith'}])`

        Notes:
        - The method assumes that `self.map` is preloaded and contains a 'features' dictionary that maps each
        field to another dictionary, mapping values to lists of indices.
        - The query is an 'AND' query, meaning that it will only return indices of records that match all
        provided key-value pairs.
        - It is assumed that the indices are unique and sorted within each list in `self.map['features']`.
        """
        indice_matrix = []
        for query_object in query_dictionary_list:
            field = list(query_object.keys())[0]
            uniq = query_object[field]
            try:
                indices = self.map["features"][field][uniq]
                indice_matrix.append(indices)
            except:
                raise KeyError(f"missing {uniq} in {field}")
        
        for arr in indice_matrix:
            arr.sort()
            current=indice_matrix[0]
            for line in indice_matrix[1:]:
                current = list(set(current) & set(line))
            current.sort()
            return current
        
    def split_batch(self,indices,batch_size):
        """
        Splits a list of indices into multiple smaller lists (batches) based on the specified batch size.

        This function iterates through the provided `indices` list and groups its elements into smaller sub-lists.
        Each sub-list (batch) will have a maximum size equal to `batch_size`. If the number of elements in `indices`
        is not a multiple of `batch_size`, the last batch may contain fewer elements.

        Parameters:
        - indices (list): A list of indices (or any items) to be split into batches.
        - batch_size (int): The maximum number of elements each batch should contain.

        Returns:
        - list of lists: A list where each element is a sub-list (batch) of `indices`, with each batch having at most
                        `batch_size` elements.

        Example:
        >>> split_batch([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        """
        lists=[[]]
        num_indices=0
        list_number=0
        for i in indices:
            if num_indices<batch_size:
                lists[list_number].append(i)
                num_indices+=1
            else:
                num_indices = 0
                list_number +=1
                lists.append([])
        return lists
    
    # retrieves a list of specified indices
    def retrieve_indices(self,indice_list):
        """
        Retrieves a list of records from an encrypted file based on a list of indices.

        Given a list of indices, this method sorts the list, then iterates through each line of the
        encrypted file located at `self.files["objects"]`. It decrypts and adds the record to the
        collection if its line number matches an index in `indice_list`. This is designed to efficiently
        retrieve a subset of records without needing to decrypt the entire file.

        Parameters:
        - indice_list (list of int): A list of integers indicating the line numbers (indices) of the
        records to be retrieved from the encrypted file.

        Returns:
        - collection (list of dict): A list of decrypted record dictionaries corresponding to the
        indices provided.

        Raises:
        - KeyError: If the 'master' key is not found in the user's validation data.
        - FileNotFoundError: If the file at `self.files["objects"]` does not exist.
        - json.JSONDecodeError: If a decrypted line from the file is not valid JSON.
        - IndexError: If an index in `indice_list` is out of range of the number of lines in the file.

        Usage:
        - To retrieve records at line numbers 2, 4, and 6, call:
        `retrieve_indices(indice_list=[2, 4, 6])`

        Notes:
        - The `validate_user` method must be successfully called prior to this method in order to
        retrieve the 'master' encryption key for decrypting records.
        - It is assumed that the records are stored in a JSON Lines format, with one JSON object per
        line and that the file contains at least as many lines as the maximum index in `indice_list`.
        - The list of indices provided should contain unique values to avoid redundant retrievals.
        """
        indice_list.sort()
        indices = indice_list
        indices_indice = 0
        current_line = 0
        collection = []
        suite = Fernet(self.validate_user()["master"])

        with open(self.files["objects"],"rb") as file:
            for line in file:
                if indices_indice<len(indices):
                    if (current_line == indices[indices_indice]):
                        record = json.loads(suite.decrypt(line).decode("utf-8"))
                        for key in list(record.keys()):
                            if key== "%BYTES%":
                                record["%BYTES%"]="Byte_Stream"
                        collection.append(record)
                        indices_indice+=1
                current_line+=1
        return collection
    
    def process_batch(self,indices, key):
        collection = []
        suite = Fernet(key)
        indices_indice = 0
        current_line = 0

        with open(self.files["objects"],"rb") as file:
            for line in file:
                if indices_indice<len(indices):
                    if (current_line == indices[indices_indice]):
                        record = json.loads(suite.decrypt(line).decode("utf-8"))
                        for key in list(record.keys()):
                            if key== "%BYTES%":
                                record["%BYTES%"]="Byte_Stream"
                        collection.append(record)
                        indices_indice+=1
                current_line+=1
        return collection
    
    def retrieve_indices_multi(self, indice_list, num_processes=2):
        # Validate user and get key
        key = self.validate_user()["master"]

        # Split the indices into batches
        indice_batches = self.split_batch(indice_list, len(indice_list) // num_processes)

        # Prepare arguments for each process
        args = [(batch, key) for batch in indice_batches]

        # Start a pool of processes and process each batch
        with Pool(num_processes) as pool:
            results = pool.starmap(self.process_batch, args)

        # Combine the results from all processes
        combined_results = [record for batch in results for record in batch]
        return combined_results
    
    # retrieves a specific indice
    def retrieve_indice(self,indice):
        """
        Retrieves a single record corresponding to the provided index from an encrypted file.

        This method is a convenience wrapper around the `retrieve_indices` method. It requests a single
        record by calling `retrieve_indices` with a list containing one index. It returns the first record
        from the returned list, which should be the only record in the list, corresponding to the provided index.

        Parameters:
        - indice (int): The index of the record to retrieve.

        Returns:
        - record (dict): The decrypted dictionary representing the single record retrieved by its index.

        Raises:
        - IndexError: If the index provided is out of the range of existing records.
        - Any exceptions raised by `retrieve_indices` will be propagated up to the caller.

        Usage:
        - To retrieve a record at index 5, call:
        `retrieve_indice(indice=5)`

        Note:
        - This method assumes that the `retrieve_indices` method is functioning correctly and that
        the underlying file contains at least as many records as the maximum index requested.
        """
        record = self.retrieve_indices([indice])[0]
        return record
    
    # returns the objects associated with the indices found using query_map
    def query_objects(self,query_dictionary_list):
        """
        Retrieves records matching the criteria specified in a query composed of field-value pairs.

        This method combines the functionalities of `query_map` and `retrieve_indices` to perform a
        two-step retrieval of records. It first determines the indices of records that match the query
        criteria specified in `query_dictionary_list` by calling `query_map`. It then retrieves the 
        actual records at those indices from the encrypted data file by calling `retrieve_indices`.

        Parameters:
        - query_dictionary_list (list of dict): A list of dictionaries, with each dictionary containing
        a 'field' and a 'unique_value' key, defining the criteria for the query.

        Returns:
        - data (list of dict): A list of decrypted records that match all the specified query criteria.

        Raises:
        - KeyError: If a query field or unique value is not found in the map, or if the necessary keys
        are not present in the user's session.
        - FileNotFoundError: If the file containing the objects data does not exist.
        - json.JSONDecodeError: If a decrypted line from the file is not valid JSON.

        Usage:
        - To retrieve objects where the field 'status' is 'active', call:
        `query_objects(query_dictionary_list=[{'field': 'status', 'unique_value': 'active'}])`

        Notes:
        - It is assumed that `query_map` returns a list of indices without duplicates and sorted in ascending order.
        - The user must be authenticated (i.e., `validate_user` has been called) before this method is used,
        to ensure that decryption keys are available.
        - The method delegates to `query_map` to find the relevant indices and to `retrieve_indices` to fetch the records.
        Any constraints or requirements of these methods also apply here.
        """
        indices = self.query_map(query_dictionary_list)
        data = self.retrieve_indices(indices)
        return data
    
    # pulls the archive from a given indice and saves it as a zip file at the given path

    def pull_archive(self, indice, filepath):
        """
        Extracts an archived file from an encrypted record by its index, unzips it, and saves the contents to a specified filepath.

        This method retrieves a single record using its index, decodes the base64-encoded content of the
        archived file contained within the record, unzips the content, and writes the extracted files to a directory at the specified
        path. This is typically used to reconstruct files previously stored in an encrypted and archived format.

        Parameters:
        - indice (int): The index of the record in the encrypted file from which to extract the archive.
        - zip_filepath (str): The directory path where the extracted files will be saved.

        Side Effects:
        - Writes to a directory specified by `zip_filepath`. If the directory already exists, its contents might be overwritten.

        Raises:
        - IndexError: If the index provided is out of the range of existing records.
        - KeyError: If the '%BYTES%' key is not present in the retrieved record.
        - binascii.Error: If base64 decoding fails.
        - IOError: If there is an issue writing to the file at `zip_filepath`.
        - zipfile.BadZipFile: If the extracted content is not a valid zip file.

        Usage:
        - To extract and unzip files from an archived record at index 10 and save them to 'path/to/extracted/', call:
        `pull_archive(indice=10, zip_filepath='path/to/extracted/')`

        Note:
        - This method assumes that the `retrieve_indices` method is available and can successfully
        retrieve the record containing the base64-encoded archive.
        - The archive is expected to be stored in the record under the key '%BYTES%' and be encoded in base64.
        """
        
        indices = [indice]
        indices_indice = 0
        current_line = 0
        collection = []
        suite = Fernet(self.validate_user()["master"])
        with open(self.files["objects"], "rb") as file:
            for line in file:
                if indices_indice < len(indices):
                    if current_line == indices[indices_indice]:
                        record = json.loads(suite.decrypt(line).decode("utf-8"))
                        collection.append(record)
                        indices_indice += 1
                current_line += 1
        
        record = collection[0]
        zip_data = base64.b64decode(record["%BYTES%"].encode("ascii"))

        # Unzipping the file
        filepath
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open("temp.zip", "wb") as temp_zip:
            temp_zip.write(zip_data)
        with zipfile.ZipFile("temp.zip", 'r') as zip_ref:
            zip_ref.extractall(filepath)
        os.remove("temp.zip")  # Clean up the temporary zip file
    
    # destroys the objects after confirming the admin policy
    def destroy(self):
        if self.validate_user()["policy"]=="admin":
            with open(self.files["objects"],"wb"):
                pass
            with open(self.files["change_log"],"wb"):
                pass
            with open(self.files["map"],"wb") as file:
                mapdata = {"objects":0,"features":{"%ADDED%":{},"%TYPE%":{}}}
                for map_param in list(self.map["features"].keys()):
                    mapdata["features"][map_param]={}
                    
                newmapdata = Fernet(self.validate_user()["master"]).encrypt(json.dumps(mapdata,indent=3).encode("utf-8"))
                file.write(newmapdata)
            self.map = mapdata
        else:
            print("This Function Requires Admin Permissions")
