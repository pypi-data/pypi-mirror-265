from playwright.sync_api import Playwright, sync_playwright, Page
from my_logtool import log
import sys
from mylib import *

OKX_SELECT = "//p[@class='_name_qdhwz_51'][text()='OKX']"
OKX_CONNECT = "//div[text()='Connect']"
OKX_PWD_INPUT = "//div[@class='okui-input-box']/input"
OKX_UNLOCK = "//span[@class='btn-content'][text()='Unlock']"
OKX_WEB_PWD_INPUT = '//*[@id="app"]/div/div/div/div[3]/form/div[1]/div/div/div/div/div/input'
OKX_WEB_UNLOCK = '//*[@id="app"]/div/div/div/div[3]/form/div[2]/div/div/div/button/span'
OKX_CONFIRM = "//span[text()='Confirm']"

class MetaMask:    
    def __init__(self, page:Page, password, wallet_url):
        self.pwd = password
        self.page = page
        self.wallet_url = wallet_url

    def oper_sleep(self, base=1000):
        self.page.wait_for_timeout(random.randint(base-100, base+100))     

    def import_by_mnemonic(self, mnemonic): 
        try:
            log.debug("import mnemonic...")
            self.page.goto(self.wallet_url)    
            # 等待页面加载完成
            logined = "//div[@class='box tabs box--flex-direction-row']"
            self.page.wait_for_load_state("domcontentloaded") 
            if wait_for_selector_attached(self.page, "//input[@id='onboarding__terms-checkbox']", timeout=5000) is None:
                if selector_is_exist(self.page, logined):
                    log.info('metamask wallet logined')   
                    return True
                else:
                    log.error(f"metamask import faile[0]")
                    return False    
            self.page.locator("//input[@id='onboarding__terms-checkbox']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[@class='button btn--rounded btn-secondary']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[@class='button btn--rounded btn-primary btn--large']").click()
            self.oper_sleep(base=500)
            eles = self.page.locator("//div[@class='MuiFormControl-root MuiTextField-root']//input").all()
            id = 0
            mnemonic_s = mnemonic.split()
            for e in eles:
                e.fill(mnemonic_s[id])
                id += 1
            self.page.locator("//button[@data-testid='import-srp-confirm']").click()
            self.oper_sleep(base=500)
            self.page.locator("//input[@data-testid='create-password-new']").fill(self.pwd)
            self.oper_sleep(base=500)
            self.page.locator("//input[@data-testid='create-password-confirm']").fill(self.pwd)
            self.oper_sleep(base=500)
            self.page.locator("//input[@type='checkbox']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[@data-testid='create-password-import']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Got it!']").click()    
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Next']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Done']").click()
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Learn more']").click()    
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Try it on MetaMask Portfolio']").click()     
            self.oper_sleep(base=500)
            self.page.locator("//button[text()='Got it']").click()   
        except Exception as r:            
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))   
            log.error(f"metamask import faile")
            return False
        log.info(f"metamask import success")
        return True

    def login_web(self):
        try:
            # 打开okx钱包页面
            log.debug('login metamask wallet')   
            self.page.goto(self.wallet_url)
            # 等待页面加载完成
            logined = "//div[@class='box tabs box--flex-direction-row']"
            self.page.wait_for_load_state("domcontentloaded") 
            if wait_for_selector_attached(self.page, "//input[@class='MuiInputBase-input MuiInput-input']", timeout=5000) is None:
                if selector_is_exist(self.page, logined):
                    log.info('metamask wallet logined')   
                    return True
                else:
                    log.error('login metamask wallet fail')
                    return False    
            # 登录钱包
            self.page.locator("//input[@class='MuiInputBase-input MuiInput-input']").fill(self.pwd)
            self.oper_sleep()
            self.page.locator("//button[@class='button btn--rounded btn-default']").click()    
            # 检查是否登录成功    
            if wait_for_selector_attached(self.page, logined, timeout=5000) is None:
                loc = self.page.locator("//p[@id='password-helper-text']")
                if loc.count():
                    log.error(f"login faile: {loc.inner_text()}")
            else:
                log.info('login metamask wallet success')
        except Exception as r:            
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))   
            log.error(f"login metamask wallet faile")
            return False
        return True
    
    def add_test_network(self, network_name, rpc, chain_id, symbol):
        try:
            log.debug("add test network...")
            self.login_web()
            self.page.locator("//div[@class='mm-box mm-box--display-flex mm-box--gap-4']//button").click()
            self.oper_sleep()
            self.page.locator("//button[@data-testid='global-menu-settings']").click()
            self.oper_sleep()
            self.page.locator("//div[@class='tab-bar__tab__content__title'][text()='Networks']").click()
            self.oper_sleep()
            self.page.locator("//button[@class='button btn--rounded btn-primary']").click()
            self.oper_sleep()
            self.page.locator("//a[@class='button btn-link']").click()
            self.oper_sleep()
            self.page.locator("//h6[text()='Network name']/../../../input").fill(network_name)
            self.oper_sleep(base=200)
            self.page.locator("//h6[text()='New RPC URL']/../../../input").fill(rpc)
            self.oper_sleep(base=200)
            self.page.locator("//h6[text()='Chain ID']/../../../input").fill(chain_id)
            self.oper_sleep(base=200)
            self.page.locator("//input[@data-testid='network-form-ticker-input']").fill(symbol)
            self.oper_sleep(base=200)
            # self.page.locator("//h6[text()='Block explorer URL']/../../../input").fill()
            # self.oper_sleep()
            self.page.locator("//button[@class='button btn--rounded btn-primary']").click()
            self.oper_sleep()
            self.page.locator("//h6[@class='mm-box mm-text mm-text--body-sm mm-box--color-primary-inverse']").click()
        except Exception as r:            
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))   
            log.error(f"add test network faile")
            return False
        log.info(f'add test network success:{rpc}')
        return True
    
    # 钱包默认操作：连接、交易都是确定
    def connect_default_oper(self, ex_page:Page, timeout=30000):   
        wait_time = 1000
        for i in range(int(timeout/wait_time)):   
            if selector_is_exist(ex_page, "//p[@class='_name_qdhwz_51'][text()='MetaMask']"):
                ex_page.locator("//p[@class='_name_qdhwz_51'][text()='MetaMask']").click() 
                log.debug('select wallet...') 
                return True
            elif selector_is_exist(ex_page, "//button[text()='Next']"):
                ex_page.locator("//button[text()='Next']").click()
                log.debug('wallet next...') 
                return True
            elif selector_is_exist(ex_page, "//button[text()='Connect']"):
                ex_page.locator("//button[text()='Connect']").click()
                log.debug('wallet connect...')   
                return True          
            else:
                log.debug('wait for wallet element...')  
                ex_page.wait_for_timeout(wait_time)
        log.error(f"unknow wallet page:{ex_page.content()}")
        ex_page.close()  

    # 钱包连接全过程
    def connect_pack(self):
        try: 
            log.debug("connect...")
            context = self.page.context
            oper = True
            while oper:
                oper = False
                page_num = len(context.pages)
                for i in range(page_num):
                    page_w = context.pages[i]
                    if page_w.title().find("Wallet") != -1 or page_w.title().find("MetaMask") != -1: 
                        oper = True
                        break
                if oper:                    
                    self.connect_default_oper(page_w)
                    self.oper_sleep(base=2000)
                    continue
                log.debug("connect complete...")
                break
        except Exception as r:
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))  
    
    # 钱包默认操作：连接、交易都是确定
    def confirm_default_oper(self, ex_page:Page, timeout=30000):  
        wait_time = 1000
        for i in range(int(timeout/wait_time)):         
            if selector_is_exist(ex_page, "//button[text()='Next']"):
                ex_page.locator("//button[text()='Next']").click() 
                log.debug('wallet Next...') 
                return True
            elif selector_is_exist(ex_page, "//button[text()='Approve']"):
                ex_page.locator("//button[text()='Approve']").click()
                log.debug('wallet Approve...') 
                return True
            elif selector_is_exist(ex_page, "//button[text()='Confirm']"):
                ex_page.locator("//button[text()='Confirm']").click()
                log.debug('wallet Confirm...')  
                return True       
            elif selector_is_exist(ex_page, "//button[text()='I want to proceed anyway']"):
                ex_page.locator("//button[text()='I want to proceed anyway']").click()
                log.debug('wallet Confirm anyway...')  
                return True 
            else:                
                log.debug('wait for wallet element...')  
                ex_page.wait_for_timeout(wait_time)
        log.error(f"unknow wallet page:{ex_page.content()}")
        ex_page.close() 
        return False
    # 钱包连接全过程
    def confirm_pack(self):
        try: 
            log.debug("confirm...")
            context = self.page.context
            oper = True
            while oper:
                oper = False
                page_num = len(context.pages)
                for i in range(page_num):
                    page_w = context.pages[i]
                    if page_w.title().find("MetaMask") != -1: 
                        oper = True
                        break
                if oper:                    
                    self.confirm_default_oper(page_w)
                    self.oper_sleep(base=2000)
                    continue
                log.debug("confirm complete...")
                break
        except Exception as r:
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))  
            return False
        return True
    
    def confirm(self):      
        if wait_for_page(self.page, title='MetaMask') is None:
            log.error("wait for wallet page fail")
            return False
        if self.confirm_pack():
            return True  
        return False

class Okx:    
    def __init__(self, page:Page, password, wallet_url):
        self.pwd = password
        self.page = page
        self.wallet_url = wallet_url        

    def oper_sleep(self):
        base = 2000
        self.page.wait_for_timeout(random.randint(base-100, base+100))
        
    def login_web(self):
        try:
            # 打开okx钱包页面
            log.debug('login okx wallet')   
            self.page.goto(self.wallet_url)
            # 等待页面加载完成
            logined = '.okui-select-value-box'
            self.page.wait_for_load_state("domcontentloaded")
            if wait_for_selector_attached(self.page, OKX_WEB_UNLOCK, timeout=5000) is None:
                if selector_is_exist(self.page, logined):
                    log.info('okx wallet logined')   
                    return True
                else:
                    log.error('login okx wallet fail')
                    return False    
            # 登录钱包
            self.page.locator(OKX_WEB_PWD_INPUT).fill(self.pwd)
            self.oper_sleep()
            self.page.locator(OKX_WEB_UNLOCK).click()    
            # 检查是否登录成功    
            if wait_for_selector_attached(self.page, logined, timeout=5000) is None:
                loc = self.page.locator('.okui-form-item-control-extra')
                if loc.count():
                    log.error(f"login faile: {loc.inner_text()}")
            else:
                log.info('login okx wallet success')
        except Exception as r:            
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))   
            log.error(f"login okx wallet faile")
            return False
        return True
        
    def login(self):
        context = self.page.context
        wallet_page = context.pages[len(context.pages)-1] 
        loc = wait_for_selector_attached(wallet_page, OKX_UNLOCK, timeout=2000)
        if loc :
            wallet_page.locator(OKX_PWD_INPUT).fill(self.pwd)
            self.oper_sleep()        
            loc.click()  
            log.debug('login okx wallet...')  
            self.oper_sleep()

    def connect(self):    
        context = self.page.context
        wallet_page = context.pages[len(context.pages)-1] 
        loc = wait_for_selector_attached(wallet_page, OKX_CONNECT, timeout=5000)
        if loc :     
            loc.click()  
            log.debug('connect okx wallet...')  
            self.oper_sleep()               

    def select(self):
        context = self.page.context
        wallet_page = context.pages[len(context.pages)-1]    # 认为最后一个弹窗为弹出的钱包
        loc = wait_for_selector_attached(wallet_page, OKX_SELECT, timeout=2000)
        if loc :
            loc.click()  
            log.debug('select okx wallet...')  
            self.oper_sleep()
        return True
    # 钱包默认操作：连接、交易都是确定
    def default_oper(self, ex_page:Page):           
        if selector_is_exist(ex_page, OKX_SELECT):
            ex_page.locator(OKX_SELECT).click() 
            log.debug('select okx wallet...') 
        elif selector_is_exist(ex_page, OKX_CONNECT):
            ex_page.locator(OKX_CONNECT).click()
            log.debug('connect okx wallet...') 
        elif selector_is_exist(ex_page, OKX_PWD_INPUT):
            ex_page.locator(OKX_PWD_INPUT).fill(self.pwd)
            self.oper_sleep()        
            ex_page.locator(OKX_UNLOCK).click()
            log.debug('unlock okx wallet...') 
        else:
            log.error(f"unknow okx wallet page:{ex_page.content()}")
            ex_page.close()  

    def clean(self):
        context = self.page.context
        page_num = len(context.pages)
        for i in range(page_num):
            ex_page = context.pages[i]
            if ex_page.title().find("Wallet") != -1: 
                self.default_oper(ex_page)
                break      # 只清理一个           
    # 钱包连接全过程
    def connect_pack(self):
        try: 
            context = self.page.context
            oper = True
            while oper:
                oper = False
                page_num = len(context.pages)
                for i in range(page_num):
                    page_okx = context.pages[i]
                    if page_okx.title().find("Wallet") != -1: 
                        oper = True
                        break
                if oper:
                    self.default_oper(page_okx)
                    self.oper_sleep()
                    continue
                break
        except Exception as r:
            s = sys.exc_info()
            log.debug("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))     

    def confirm(self):
        context = self.page.context
        wallet_page = context.pages[len(context.pages)-1]        
        loc = wait_for_selector_attached(wallet_page, OKX_CONFIRM, timeout=10000) 
        if loc:
            loc.click()
            log.info("okx confirm success")
            return True   
        log.error("okx confirm faile")
        return False

if __name__ == "__main__":       
    from bitdemo.bit_api import *
    import myconfig
    with sync_playwright() as playwright:           
        res = openBrowser(id="3547827ebf3a4253aa01f6a0e13ba95d")
        ws = res['data']['ws']
        log.debug(f"ws address ==>>> {ws}")

        chromium = playwright.chromium
        browser = chromium.connect_over_cdp(ws)
        default_context = browser.contexts[0]
        page = default_context.new_page()
        mm = MetaMask(page, myconfig.WALLET_PWD, myconfig.WALLET_URL)
        mm.login_web()



