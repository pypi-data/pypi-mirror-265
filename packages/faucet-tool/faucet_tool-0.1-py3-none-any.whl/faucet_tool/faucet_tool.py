from playwright.sync_api import Playwright, sync_playwright, expect, Page, ElementHandle
import bitbrowser_api
from my_logtool import log
import sys
from mylib import *
def get_faucet_artio(page:Page, wallet): 
    trycount = 3
    while trycount:
        trycount -= 1  
        try:
            # 打开水龙头页面    
            page.goto('https://artio.faucet.berachain.com/')
            # 等待页面加载完成
            page.wait_for_load_state("domcontentloaded")
            log.debug('page loaded') 
            # 条款
            loc = page.get_by_label("I have read, understood, and")
            if loc.count():
                loc.click()
                oper_sleep(page)
                page.get_by_role("button", name="I AGREE").click()
                oper_sleep(page)

            # 填入钱包地址
            page.locator('.relative.w-full > input').fill(wallet)
            # 校验真人            
            floc = page.frame_locator("iframe[title='Widget containing a Cloudflare security challenge']")
            floc.get_by_label('Verify you are human').click()
            oper_sleep(page)

            # 点击领水
            page.locator('button[type=submit]').click() 
        except Exception as r:
            s = sys.exc_info()
            log.error("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)) 
            continue
        else:
            #成功点击领水
            loc = wait_for_selector_attached(page, '.leading-tight.tracking-tight')
            if loc is None:
                log.info(f'get faucet of artio fail')  
                continue
            else:            
                log.info(f'get faucet({wallet}) of artio success:{loc.inner_text()}')  
                return True   
    return False

if __name__ == "__main__":   
    with sync_playwright() as playwright:   
        browser_id = "8e897dc29a2b4af69145b8ffb75dea85"
        session_val = generate_random_str(randomlength=12, base_str='abcdef0123456789')
        b = bitbrowser_api.BitBrowser(
            url="http://127.0.0.1:54345",
            headers={'Content-Type': 'application/json'},
            id=browser_id,
            proxy_type='socks5',
            proxy_host='c9234a9e61813939.yiu.us.ip2world.vip',
            proxy_port=6001,
            proxy_user=f'dynamic-zone-resi-region-us-session-{session_val}-sessTime-30',
            proxy_pwd='dynamic'
        )  
        b.open()
        chromium = playwright.chromium
        browser = chromium.connect_over_cdp(b.ws)
        context = browser.contexts[0]
        log.debug(f"playwright connect:{b.ws}")
        page = context.new_page()
        get_faucet_artio(page, "0x00")
        
            
        


    

