from django.shortcuts import render,redirect , HttpResponse
from .forms import ClientLogin,ClientDetailForm
from .forms import *
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from myapp.models import ClientDetail , ClientSignal
from django.utils import timezone    
import datetime
from django.contrib import messages
from algosms import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime, timedelta
# Create your views here.
my_global_variable = None
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def logoutAdmin(request):
    if 'cadmin_id' in request.session:
        del request.session['cadmin_id']
    logout(request)
    return redirect('admin_login')

def logoutUser(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        client_user = ClientDetail.objects.filter(user_id=user_id).first()
        del request.session['user_id']
    else:
        client_user = None

    logout(request)
    # You can pass client_user to the template if needed, but typically on logout you just redirect.
    return redirect('client_login')


def client_base(request):
    user_id = request.session.get('user_id')
    if user_id:
        client_user = ClientDetail.objects.filter(user_id=user_id).first()
        if client_user:
            return render(request, 'client_base.html', {'client_user': client_user})
        else:
            # Handle the case where the client user is not found
            return redirect('client_login')
    else:
        return redirect('client_login')

   
    



from django.contrib.auth.decorators import login_required

@login_required
def client_dashboard(request):
    # Your view logic here
    return render(request, 'client_dashboard.html')

from django.utils import timezone

def client_login(request):

    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                user_id = ClientDetail.objects.get(email=user.email)
                # Check if last login date is today or later
                if user.last_login.date() >= timezone.now().date():
                    request.session['user_id'] = user_id.user_id

                    alls = SYMBOL.objects.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.user_id , SYMBOL = s.SYMBOL)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.user_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.user_id,
                                SYMBOL = s.SYMBOL,
                                QUANTITY = q
                            )
                            

                    return redirect('/dashboard/')
                else:
                    return redirect('/?msg=your plane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
         #   return HttpResponse('email no register')
            return redirect('/?msg=Email no register') 
     
    return render(request,'client_login.html', {'msg':msg})

# def admin_dashboard(request):
#     if not request.user.is_authenticated:
#         return redirect('admin_login')
    # if Account.objects.filter(user_id= request.user.user_id, is_client=True):
    #     client = Client.objects.all()
    #     LeaveRequests = TLeave.objects.filter(is_approved=0)
    #     return render(request,'admin_dashboard.html', context={'allEmp':allEmp, 'LeaveR':LeaveRequests})
    # else:
    #     messages.info(request, 'You Are Not Authorized To Access That Page')
        # return redirect('index')
    # return render(request,'admin_dashboard.html')  
@login_required(login_url='adminlogin')
def admin_dashboard(request):
    # For cards on dashboard
    clientcount = ClientDetail.objects.all().count()
    
    # For recent order tables
    total_live_account = ClientDetail.objects.filter(clint_status='live').count()
    total_demo_account = ClientDetail.objects.filter(clint_status='demo').count()
    total_licence = ClientDetail.objects.filter(clint_status='licence').count()
    total_2days_service = ClientDetail.objects.filter(clint_status='2days_service').count()
    
    active_live_account = ClientDetail.objects.filter(clint_status='active_live').count()
    active_demo_account = ClientDetail.objects.filter(clint_status='active_demo').count()
    remaining_licence = ClientDetail.objects.filter(clint_status='remaining_licence').count()
    active_2days_service = ClientDetail.objects.filter(clint_status='active_2days_service').count()
    
    expired_total_account = ClientDetail.objects.filter(clint_status='expired_live').count()
    expired_demo_account = ClientDetail.objects.filter(clint_status='expired_demo').count()
    used_licence = ClientDetail.objects.filter(clint_status='used_licence').count()
    total_converted_accounts = ClientDetail.objects.filter(clint_status='converted').count()

    mydict = {
        'clientcount': clientcount,
        'total_live_account': total_live_account,
        'total_demo_account': total_demo_account,
        'total_licence': total_licence,
        'total_2days_service': total_2days_service,
        'active_live_account': active_live_account,
        'active_demo_account': active_demo_account,
        'remaining_licence': remaining_licence,
        'active_2days_service': active_2days_service,
        'expired_total_account': expired_total_account,
        'expired_demo_account': expired_demo_account,
        'used_licence': used_licence,
        'total_converted_accounts': total_converted_accounts,
    }
    
    return render(request, 'admin_dashboard.html', context=mydict)


       

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils import timezone
scheduler = BackgroundScheduler()

# Function to create attendance records for employees
@transaction.atomic
def symbol_inactive():
    timezone.activate('Asia/Kolkata')
    ss = Client_SYMBOL_QTY.objects.all()
    for s in ss:
        s.trade = None
        s.save()       
# Set the job to run every day at 12:00 AM
# scheduler.add_job(symbol_inactive, 'cron', hour=0, minute=1)
# scheduler.start()


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"  
        except:
            error = "yes"          
    return render(request,'admin_login.html', locals()) 


from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def create_superuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                User.objects.create_superuser(username=username, email=email, password=password1)
                return redirect('admin_login')
                # return HttpResponse('Superuser created successfully!')
            except:
                return HttpResponse('Error creating superuser. Please try again.')
        else:
            return HttpResponse('Passwords do not match. Please try again.')
    else:
        return render(request, 'admin_register.html')
    
    
def admin_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return render(request, 'change_password.html', {'msg': 'Password updated successfully', 'error': 'no'})
            else:
                return render(request, 'change_password.html', {'msg': 'New Password and Confirm Password fields do not match', 'error': 'yes'})
        else:
            return render(request, 'change_password.html', {'msg': 'Your current password is wrong', 'error': 'not'})
    else:
        return render(request, 'change_password.html', {})    


# =====================================================================================

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['fname']
        ln = request.POST['lname']
        mo = request.POST['mobile']
        em = request.POST['email']
        fromd = request.POST['fromdate']
        tod = request.POST['todate']
        pwd = request.POST['pwd']
        print(fromd, ' to ', tod)
        try:
            try:
                u = ClientDetail.objects.get(email=em)
                return render(request,'register.html',{'msg': 'email all ready registration '}) 
            except:    
         #   user = User.objects.create_user(first_name=fn,last_name=ln,username=em,password=pwd)
                ClientDetail.objects.create(
                                        name_first = fn,
                                        name_last = ln,
                                        email = em,
                                        password = pwd,
                                        phone_number = mo,
                                        date_joined	= fromd,
                                        last_login	= tod
                                                    )
                # Construct the email message
                subject = 'your email paswword'
                message = f'Name: {fn,ln}\nEmail: {em}\nPassword: {pwd}\n\nphone:\n{mo}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [em]  # Add recipient email addresses here
                
             
                try:
                    # Send email
                    send_mail(subject, message, email_from, recipient_list)
                #    send_mail(subject, body, from_email, to_email, fail_silently=False)
                    return redirect('/')
                except Exception as e:
                    # Handle any errors
                #  return HttpResponse('error.html', {'error': str(e)})
                   # return render(request, 'contact.html',{'msg':f'{e}'})
                    return render(request,'register.html',{'msg': f'{e}'}) 
                
        except Exception as e:
            return render(request,'register.html',{'msg': f'error {e}'}) 
    return render(request,'register.html',)    


def client_list(request):
    # try:        
        clientdetail = ClientDetail.objects.all()
        return render(request, 'client_list.html', {'clientdetail': clientdetail})
    # except:
    #     return redirect('admin_login')


def update_client(request, user_id):
    # Retrieve the symbol object from the database
    clientdetail = get_object_or_404(ClientDetail, user_id=user_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = ClientDetailForm(request.POST, instance=clientdetail)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('client_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = ClientDetailForm(instance=clientdetail)
    
    return render(request, 'update_clientdetail.html', {'form': form, 'clientdetail': clientdetail})


def delete_client(request, user_id):
    clientdetail = ClientDetail.objects.get(user_id=user_id)
    if request.method == 'POST':
        clientdetail.delete()
        return redirect('client_list')  # Redirect to the symbol list page after deletion
    return render(request, 'delete_clientdetail.html', {'clientdetail': clientdetail})



 



# ============================================Admin  ==========================================
# =============================================================================================

# Function to handle admin messages
import random
import string


def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id
#ids = None
def admin_message(request):
    error = ""
    symbols = SYMBOL.objects.all()  # Fetch all SYMBOL objects
    user = request.user
    current_date = timezone.now().date()
    d = request.session.get('message_id')
    if request.method == "POST":
        if request.user.is_authenticated:
            client_signals = ClientSignal.objects.filter( message_id = d , ids = 'No')
            
            user = request.user
            symbol_name = request.POST['symbol']  # Get the symbol name from the form
            sy = get_object_or_404(SYMBOL, SYMBOL=symbol_name)  # Fetch the corresponding SYMBOL instance
            # sy = request.POST['symbol']
            ty = request.POST['type']
         
            qty_str = request.POST['quantity']
         
            if ty == 'BUY_EXIT' or ty == 'SELL_EXIT':
                    for client_signal in client_signals:
                        print('test for ')
                        if qty_str.strip():  # Check if quantity string is not empty or only whitespace
                            qty = float(qty_str)
                        elif ty == 'BUY_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = float(request.POST['exit_price'])

                        elif ty == 'SELL_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = float(request.POST['exit_price'])    

                        else:
                            qty = 0 # Set qty to a default value or handle it according to your logic
                            enp = float(request.POST['entry_price'])
                            exp =  None
                    
                    
                        if ty == 'BUY_EXIT':
                        #    print('BUY_EXIT')
                            prloss = (float(exp) - float(enp)) * qty*100
                            t = ClientSignal.objects.filter( TYPE = 'BUY_EXIT' , client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = float(total) + float(prloss)
                            print(total_pl)

                        elif ty == 'SELL_EXIT':
                            print('SELL_EXIT')
                            prloss = (float(enp) - float(exp)) * 100*qty
                            t = ClientSignal.objects.filter( TYPE = 'SELL_EXIT' ,client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                            #    print(total)
                            
                        
                            total_pl = float(total) + float(prloss)
                        #    print(total_pl)
                            
                    
                            
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                    ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss, 
                                                    cumulative_pl=total_pl, created_at=timezone.now(),
                                                    message_id = client_signal.message_id ,client_id  = client_signal.client_id )
                

            else:
                    qty = 0 # Set qty to a default value or handle it according to your logic
                    enp = float(request.POST['entry_price'])
                    exp =  None
                    prloss = None
                    total_pl = None                                    
                    if ty == 'BUY_ENTRY' or ty == 'SELL_ENTRY':
                        
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, admin = 'admin',TYPE=ty, QUANTITY=qty, 
                                                ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=prloss, 
                                                cumulative_pl=total_pl, created_at=timezone.now())
                        i = generate_unique_id()
                        creat.message_id = creat.id
                        creat.ids = i 
                        creat.save()      
                        request.session['message_id'] = creat.id
                    #    request.session['ids'] = i
                        global my_global_variable
                        my_global_variable = i
                        
                        error = "no"
                        result = add_singnal_qty(request)
    return render(request, 'admin_messages.html',{'symbols': symbols, 'error': error})
########################

''' 
def admin_message(request):
    error = ""
    user = request.user
    current_date = timezone.now().date()
    d = request.session.get('message_id')
    if request.method == "POST":
        if request.user.is_authenticated:
            client_signals = ClientSignal.objects.filter( message_id = d , ids = 'No')
            
            user = request.user
            sy = request.POST['symbol']
            ty = request.POST['type']
         
            qty_str = request.POST['quantity']
         
            if ty == 'BUY_EXIT' or ty == 'SELL_EXIT':
                    for client_signal in client_signals:
                        if qty_str.strip():  # Check if quantity string is not empty or only whitespace
                            qty = int(qty_str)
                        elif ty == 'BUY_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = int(request.POST['exit_price'])

                        elif ty == 'SELL_EXIT':
                            qty = client_signal.QUANTITY     
                            enp = client_signal.ENTRY_PRICE
                            exp = int(request.POST['exit_price'])    

                        else:
                            qty = 0 # Set qty to a default value or handle it according to your logic
                            enp = int(request.POST['entry_price'])
                            exp =  None
                    
                    
                    
                        if ty == 'BUY_EXIT':
                            print('BUY_EXIT')
                            prloss = (float(exp) - float(enp)) * qty
                            t = ClientSignal.objects.filter( TYPE = 'BUY_EXIT' , client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = int(total) + int(prloss)
                            print(total_pl)

                        elif ty == 'SELL_EXIT':
                            print('SELL_EXIT')
                            prloss = (float(exp) - float(enp)) * qty
                            t = ClientSignal.objects.filter( TYPE = 'SELL_EXIT' ,client_id = client_signal.client_id, created_at__date=current_date )
                            total = 0
                            for p in t:
                                total += p.profit_loss
                                print(total)
                            
                        
                            total_pl = int(total) + int(prloss)
                            print(total_pl)
                            
                    
                            
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                    ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss, 
                                                    cumulative_pl=total_pl, created_at=timezone.now(),
                                                    message_id = client_signal.message_id ,client_id  = client_signal.client_id )
                

            else:
                    qty = 0 # Set qty to a default value or handle it according to your logic
                    enp = int(request.POST['entry_price'])
                    exp =  None
                    prloss = None
                    total_pl = None                                    
                    if ty == 'BUY_ENTRY' or ty == 'SELL_ENTRY':
                        
                        creat = ClientSignal.objects.create(user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty, 
                                                ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=prloss, 
                                                cumulative_pl=total_pl, created_at=timezone.now())
                        i = generate_unique_id()
                        creat.message_id = creat.id
                        creat.ids = i
                        creat.save()      
                        request.session['message_id'] = creat.id
                    #    request.session['ids'] = i
                        global my_global_variable
                        my_global_variable = i
                       
                        error = "no"
         
    return render(request, 'admin_messages.html', )
'''
def admin_signals(request):
    # Check if the user is authenticated and is an admin
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('admin_login')

    # Get the current date
    current_date = timezone.now().date()

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = ClientSignalForm(request.POST)
        if form.is_valid():
            # If form is valid, save the form data without associating it with any client
            # Adjust this part according to your form and model
            form.save()
            return redirect('admin_signal_center')  # Redirect to the same page after form submission
    else:
        # If the request method is not POST, instantiate a new form
        form = ClientSignalForm()

    # Retrieve records for the current day only
    signals = ClientSignal.objects.filter(created_at__date=current_date).order_by('-created_at')

    # Render the admin_signal_center.html template with the form and signals
    return render(request, 'admin_signals.html', {'form': form, 'signals': signals})

# def admin_signals(request):
#     try:
#         user = request.session.get('user')
#         user = ClientDetail.objects.get(user=user)

#         # Filter signals for today and order them by created_at in descending order
#         today = date.today()
#         signals_today = ClientSignal.objects.filter(user=user, created_at__date=today).order_by('-created_at')

#         dt = {
#             "s": signals_today,
#         }
#         return render(request, 'admin_signals.html', dt)
#     except:
#         return redirect('admin_login')







def admin_thistory(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    clientsignal = ClientSignal.objects.all()
    return render(request,'admin_thistory.html',locals())

def admin_tstatus(request):
    return render(request,'admin_tstatus.html')

def admin_client(request):
    return render(request,'admin_client.html')

# def admin_help_center(request):
#     return render(request,'admin_help_center.html')


def client_dashboard(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)
        
        
        current_date = timezone.now().date()
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id = user_id)
        
        if request.method == 'POST':
            print('pst')
            # XAUUSD
            q1 = request.POST.get('QUANTITY1')
            o1 = request.POST.get('ORDER_TYPE1')
            t1 = request.POST.get('TRADING1')
            print(q1,o1,t1)
            # USOIL
            q2 = request.POST.get('QUANTITY2')
            o2 = request.POST.get('ORDER_TYPE2')
            t2 = request.POST.get('TRADING2')
            print(q2,o2,t2)
            # EURUSD
            q3 = request.POST.get('QUANTITY3')
            o3 = request.POST.get('ORDER_TYPE3')
            t3 = request.POST.get('TRADING3')
            print(q3,o3,t3)
            # USDJPY
            q4 = request.POST.get('QUANTITY4')
            o4 = request.POST.get('ORDER_TYPE4')
            t4 = request.POST.get('TRADING4')
            print(q4,o4,t4)
            # GBPUSD
            q5 = request.POST.get('QUANTITY5')
            o5 = request.POST.get('ORDER_TYPE5')
            t5 = request.POST.get('TRADING5')
            print(q5,o5,t5)
            # EURJPY
            q6 = request.POST.get('QUANTITY6')
            o6 = request.POST.get('ORDER_TYPE6')
            t6 = request.POST.get('TRADING6')
            print(q6,o6,t6)
            # AUDNZD
            q7 = request.POST.get('QUANTITY7')
            o7 = request.POST.get('ORDER_TYPE7')
            t7 = request.POST.get('TRADING7')
            print(q7,o7,t7)
            # GBPNZD
            q8 = request.POST.get('QUANTITY8')
            o8 = request.POST.get('ORDER_TYPE8')
            t8 = request.POST.get('TRADING8')
            print(q8,o8,t8)
            # USDCHF
            q9 = request.POST.get('QUANTITY9')
            o9 = request.POST.get('ORDER_TYPE9')
            t9 = request.POST.get('TRADING9')
            print(q9,o9,t9)
             # GBPCAD
            q10 = request.POST.get('QUANTITY10')
            o10 = request.POST.get('ORDER_TYPE10')
            t10 = request.POST.get('TRADING10')
            print(q10,o10,t10)
            # EURAUD
            q11 = request.POST.get('QUANTITY11')
            o11 = request.POST.get('ORDER_TYPE11')
            t11 = request.POST.get('TRADING11')
            print(q11,o11,t11)
             # AUDNZD
            q12 = request.POST.get('QUANTITY12')
            o12 = request.POST.get('ORDER_TYPE12')
            t12 = request.POST.get('TRADING12')
            print(q12,o12,t12)
            # EURGBP
            q13 = request.POST.get('QUANTITY13')
            o13 = request.POST.get('ORDER_TYPE13')
            t13 = request.POST.get('TRADING13')
            print(q13,o13,t13)
            # NZDUSD
            q14 = request.POST.get('QUANTITY14')
            o14 = request.POST.get('ORDER_TYPE14')
            t14 = request.POST.get('TRADING14')
            print(q14,o14,t14)
            # USDCAD
            q15 = request.POST.get('QUANTITY15')
            o15 = request.POST.get('ORDER_TYPE15')
            t15 = request.POST.get('TRADING15')
            print(q15,o15,t15)
            # AUDUSD
            q16 = request.POST.get('QUANTITY16')
            o16 = request.POST.get('ORDER_TYPE16')
            t16 = request.POST.get('TRADING16')
            print(q16,o16,t16)
            # GBPJPY
            q17 = request.POST.get('QUANTITY17')
            o17 = request.POST.get('ORDER_TYPE17')
            t17 = request.POST.get('TRADING17')
            print(q17,o17,t17)
            # AUDJPY
            q18 = request.POST.get('QUANTITY18')
            o18 = request.POST.get('ORDER_TYPE18')
            t18 = request.POST.get('TRADING18')
            print(q18,o18,t18)
            value = my_global_variable
            try:
                
                
                Client_symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id = user_id)
                
                for q in Client_symbol_qty:
                    if q.SYMBOL == 'XAUUSD':
                        if t1 == 'on':
                            q.QUANTITY = float(q1)
                            q.trade = t1
                            q.save() 
                        else:
                            q.trade = t1 
                            q.save()    

                    elif q.SYMBOL == 'USOIL':
                        if t2 == 'on':
                            q.QUANTITY = float(q2)
                            q.trade = t2 
                            q.save()  
                        else:
                            q.trade = t2 
                            q.save()        

                    elif q.SYMBOL == 'EURUSD':
                        if t3 == 'on':
                            q.QUANTITY = float(q3)
                            q.trade = t3  
                            q.save() 
                        else:
                            q.trade = t3 
                            q.save()      

                    elif q.SYMBOL == 'USDJPY':
                        if t4 == 'on':
                            q.QUANTITY = float(q4)
                            q.trade = t4  
                            q.save() 
                        else:
                            q.trade = t4 
                            q.save()      
                        
                    elif q.SYMBOL == 'EURJPY':
                        if t6 == 'on':
                            q.QUANTITY = float(q6)
                            q.trade = t6 
                            q.save()    
                        else:
                            q.trade = t6 
                            q.save() 
                            
                    elif q.SYMBOL == 'AUDNZD':
                        if t7 == 'on':
                            q.QUANTITY = float(q7)
                            q.trade = t7 
                            q.save()    
                        else:
                            q.trade = t7 
                            q.save() 
                            
                    elif q.SYMBOL == 'GBPNZD':
                        if t8 == 'on':
                            q.QUANTITY = float(q8)
                            q.trade = t8 
                            q.save()    
                        else:
                            q.trade = t8 
                            q.save()    
                            
                    elif q.SYMBOL == 'USDCHF':
                        if t9 == 'on':
                            q.QUANTITY = float(q9)
                            q.trade = t9 
                            q.save()    
                        else:
                            q.trade = t9 
                            q.save()                 
                    
                    elif q.SYMBOL == 'GBPCAD':
                        if t10 == 'on':
                            q.QUANTITY = float(q10)
                            q.trade = t10 
                            q.save()    
                        else:
                            q.trade = t10 
                            q.save() 
                            
                    elif q.SYMBOL == 'EURAUD':
                        if t11 == 'on':
                            q.QUANTITY = float(q11)
                            q.trade = t11 
                            q.save()    
                        else:
                            q.trade = t11 
                            q.save()                
                    
                    elif q.SYMBOL == 'AUDNZD':
                        if t12 == 'on':
                            q.QUANTITY = float(q12)
                            q.trade = t12 
                            q.save()    
                        else:
                            q.trade = t12 
                            q.save()               
                    
                    elif q.SYMBOL == 'EURGBP':
                        if t13 == 'on':
                            q.QUANTITY = float(q13)
                            q.trade = t13 
                            q.save()    
                        else:
                            q.trade = t13 
                            q.save()          
                    
                    elif q.SYMBOL == 'NZDUSD':
                        if t14 == 'on':
                            q.QUANTITY = float(q14)
                            q.trade = t14 
                            q.save()    
                        else:
                            q.trade = t14 
                            q.save()             

                    elif q.SYMBOL == 'USDCAD':
                        if t15 == 'on':
                            q.QUANTITY = float(q15)
                            q.trade = t15 
                            q.save()    
                        else:
                            q.trade = t15 
                            q.save()          
                    
                    elif q.SYMBOL == 'AUDUSD':
                        if t16 == 'on':
                            q.QUANTITY = float(q16)
                            q.trade = t16 
                            q.save()    
                        else:
                            q.trade = t16 
                            q.save() 
                            
                    elif q.SYMBOL == 'GBPJPY':
                        if t17 == 'on':
                            q.QUANTITY = float(q17)
                            q.trade = t17 
                            q.save()    
                        else:
                            q.trade = t17 
                            q.save()          
                    
                    elif q.SYMBOL == 'AUDJPY':
                        if t18 == 'on':
                            q.QUANTITY = float(q18)
                            q.trade = t18 
                            q.save()    
                        else:
                            q.trade = t18 
                            q.save()  
                    
                return redirect('client_dashboard')
            except Exception as e:               
                error = str(e)
                print(error) 


        return render(request,'client_dashboard.html',{'signals':filtered_signals})
    except:
        return redirect('login')

def add_singnal_qty(request):
    Client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    value = my_global_variable
    try:
        client_signal = ClientSignal.objects.get(ids= value) 
        for q in Client_symbol_qty:
            print('for tes qq', q.SYMBOL)
            print('for tes cc',client_signal.SYMBOL)
            print('for')
            if q.trade == 'on':
                print('on')    
                if str(q.SYMBOL) == str(client_signal.SYMBOL):
                    print('symbol')
                    print(q.SYMBOL)
                    print(client_signal.SYMBOL)
                    print('creat singnal')
                    creat = ClientSignal.objects.create(
                        user=client_signal.user,
                        SYMBOL=client_signal.SYMBOL,
                        TYPE=client_signal.TYPE,
                        ENTRY_PRICE=client_signal.ENTRY_PRICE,
                        ids = 'No',
                        QUANTITY=q.QUANTITY,
                        message_id = client_signal.message_id,
                        client_id = q.client_id,
                        created_at = timezone.now()
                    )

                    
        return HttpResponse('pass function')    
    except Exception as e:
        error = str(e)
        print(error)   
        return HttpResponse(f'error = {e}') 

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ClientSignal
from django.contrib import messages
from datetime import datetime, date
from django.http import HttpResponseNotFound

# client_signals client get method          
def client_signals(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        dt = {
            "s": signals_today,
        
        }
        return render(request, 'client_signals.html', dt)
    except:
        return redirect('client_login')
        
    
   
    
from django.db.models import Sum

def client_trade_history(request):
    try:
        user_id = request.session.get('user_id')
        client_user = ClientDetail.objects.get(user_id=user_id)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('created_at')
        # signals_today = ClientSignal.objects.filter(client_id=user_id, created_at__date=today).order_by('-created_at')

        # Calculate total profit and loss for today
        total_cumulative_pl = signals_today.aggregate(total_pl=Sum('cumulative_pl'))['total_pl']

        dt = {
            "s": signals_today,
            "total_cumulative_pl": total_cumulative_pl
        }
        return render(request, 'client_thistory.html', dt)
    except:
        return redirect('client_login')




def change_password(request):
    try:
        #    print('test form' ) 
        user_id = request.session.get('user_id')
    
        client_user = ClientDetail.objects.get(user_id=user_id)
        if request.method == "POST":
            c = request.POST['currentpassword']
            n = request.POST['newpassword']
            f = request.POST['confirmpassword']

            if c == client_user.password and n == f:
                client_user.password = n
                client_user.save()
                return redirect('/?msg=chenge password')  
            else:
                return render(request,'client_change_password.html',{'msg':'samthing wrong'})    
        return render(request,'client_change_password.html',locals(),)       
    except:
        return redirect('client_login')        


def admin_change_password(request):
    if not request.user.is_authenticated:
        return redirect('client_login')
    error = ""
    user = request.user
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        
        try:
            if user.check_password(c):
                user.set_password(n)
                user.save()
                error = "no"  
            else:
                error = "not"    
        except:
            error = "yes"
    return render(request,'admin_change_password.html',locals(),{'error': error}) 


def Settings(request):
    return render(request,'settings.html')

# ===============================Symbolic qty =============================
from django.shortcuts import render, redirect, get_object_or_404
from .models import Client_SYMBOL_QTY
from .forms import Client_SYMBOL_QTYForm

def create_client_symbol_qty(request):
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')  # Redirect to the list view
    else:
        form = Client_SYMBOL_QTYForm()
    return render(request, 'create_client_symbol_qty.html', {'form': form})

def client_symbol_qty_list(request):
    client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    return render(request, 'client_symbol_qty_list.html', {'client_symbol_qty': client_symbol_qty})

def edit_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        form = Client_SYMBOL_QTYForm(request.POST, instance=client_symbol_qty)
        if form.is_valid():
            form.save()
            return redirect('client_symbol_qty_list')
    else:
        form = Client_SYMBOL_QTYForm(instance=client_symbol_qty)
    return render(request, 'edit_client_symbol_qty.html', {'form': form})

def delete_client_symbol_qty(request, pk):
    client_symbol_qty = get_object_or_404(Client_SYMBOL_QTY, pk=pk)
    if request.method == 'POST':
        client_symbol_qty.delete()
        return redirect('client_symbol_qty_list')
    return render(request, 'delete_client_symbol_qty.html', {'client_symbol_qty': client_symbol_qty})


# ========================== SYMBOL ====================================================

# =======================================================================================
from .forms import SymbolForm

def symbol_list(request):
    symbols = SYMBOL.objects.all()
    return render(request, 'symbol_list.html', {'symbols': symbols})

def create_symbol(request):
    if request.method == 'POST':
        form = SymbolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('symbol_list')
    else:
        form = SymbolForm()
    return render(request, 'create_symbol.html', {'form': form})

def update_symbol(request, symbol_id):
    # Retrieve the symbol object from the database
    symbol = get_object_or_404(SYMBOL, id=symbol_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = SymbolForm(request.POST, instance=symbol)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('symbol_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = SymbolForm(instance=symbol)
    
    return render(request, 'update_symbol.html', {'form': form, 'symbol': symbol})



def delete_symbol(request, symbol_id):
    symbol = SYMBOL.objects.get(id=symbol_id)
    if request.method == 'POST':
        symbol.delete()
        return redirect('symbol_list')  # Redirect to the symbol list page after deletion
    return render(request, 'delete_symbol.html', {'symbol': symbol})



# ==================================  Feedback=============================================

# =============================================================================== =======

from django.shortcuts import render, redirect
from .models import HelpMessage
from .forms import HelpMessageForm


def client_help_center(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('client_login')  # Redirect to login if user_id is not in session

    try:
        client_detail = ClientDetail.objects.get(user_id=user_id)
    except ClientDetail.DoesNotExist:
        return redirect('client_login')  # Redirect to login if the client does not exist

    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            help_message = form.save(commit=False)
            help_message.user_id = client_detail  # Set the user_id field to the client_detail instance
            help_message.save()
            return redirect('client_help_center')  # Redirect to the same page or a thank you page
    else:
        form = HelpMessageForm()

    messages = HelpMessage.objects.filter(user_id=client_detail)

    return render(request, 'client_help_center.html', {'form': form, 'messages': messages})


def admin_signals(request):
    try:
        user = request.session.get('user')
        user = ClientDetail.objects.get(user=user)

        # Filter signals for today and order them by created_at in descending order
        today = date.today()
        signals_today = ClientSignal.objects.filter(user=user, created_at__date=today).order_by('-created_at')

        dt = {
            "s": signals_today,
        }
        return render(request, 'admin_signals.html', dt)
    except:
        return redirect('admin_login')


# def admin_help_center(request):
#     # Retrieve all HelpMessage objects ordered by timestamp in descending order
#     messages = HelpMessage.objects.all().order_by('-timestamp')
#     # Pass the messages to the admin_help_center.html template
#     return render(request, 'admin_help_center.html', {'messages': messages})
def admin_help_center(request):
    # Get the user_id from the session
    user_id = request.session.get('user_id')
    
    # If user_id is not found in the session, redirect to the admin login page
    if not user_id:
        return redirect('admin_login')
    
    # Check if the user is an admin (you might have a way to distinguish admins from clients)
    # For example, if admins have a specific role in your system:
    if not request.user.is_superuser:
        return redirect('admin_login')

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            # If form is valid, save the form data without associating it with any client
            help_message = form.save(commit=False)
            help_message.save()
            return redirect('admin_help_center')  # Redirect to the same page after form submission
    else:
        # If the request method is not POST, instantiate a new form
        form = HelpMessageForm()

    # Retrieve all HelpMessage objects (for admins, not associated with any client) in descending order by timestamp
    messages = HelpMessage.objects.all().order_by('-timestamp')

    # Render the admin_help_center.html template with the form and messages
    return render(request, 'admin_help_center.html', {'form': form, 'messages': messages})


# def client_tstatus(request):
#     return render(request,'client_tstatus.html')

def client_tstatus(request):
    try:
        # Your existing code to get the client's IP address
        client_ip = request.META.get('REMOTE_ADDR', None)
        
        # Your logic for client_tstatus
        # user_id = request.session.get('user_id')
        # clientdetail = ClientDetail.objects.filter(user_id=user_id, created_at__date=date.today()).order_by('-created_at')

        dt = {"client_ip": client_ip}
        return render(request, 'client_tstatus.html', dt)
    except:
        return redirect('client_login')
    

# def multibank(request):
#     return render(request,'multibank.html')

def multibank(request):

    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                user_id = ClientDetail.objects.get(email=user.email)
                # Check if last login date is today or later
                if user.last_login.date() >= timezone.now().date():
                    request.session['user_id'] = user_id.user_id

                    alls = SYMBOL.objects.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.user_id , SYMBOL = s.SYMBOL)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.user_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.user_id,
                                SYMBOL = s.SYMBOL,
                                QUANTITY = q
                            )
                            

                    return redirect('/dashboard/')
                else:
                    return redirect('/?msg=your plane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
         #   return HttpResponse('email no register')
            return redirect('/?msg=Email no register') 
     
    return render(request,'multibank.html', {'msg':msg})




