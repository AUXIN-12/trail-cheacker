import tls_client
import threading
import time
import json
import random
import os
from typing import Optional, Dict, List, Tuple
from helpers.logging.logger import Console

class DiscordTrialChecker:
    
    def __init__(self):
        self.console = Console()
        self.proxies: List[str] = []
        self.results = {
            'trial': [],
            'invalid': [],
            'no_trial': [],
            'errors': [],
            'one_month_trial': [],
            'two_week_trial': [],
            'discount_tokens': []
        }
        self.lock = threading.Lock()
        self.file_lock = threading.Lock()
        self.thread_count = 1
        self.checked_count = 0
        self.trial_count = 0
        self.config = self.load_config()
        self.output_folder = self.create_output_folder()
        
        self.url = "https://discord.com/api/v9/users/@me/billing/user-offer"
        
        self.headers_template = {
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'authorization': '',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'priority': 'u=1, i',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-discord-timezone': 'Asia/Calcutta',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzOC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTM4LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQxNzI2NiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6Ijg4ZDM3ZTA5LWNhNTEtNDNlYi05NDRmLTcwMmI5OGNmNDNiOSIsImNsaWVudF9hcHBfc3RhdGUiOiJ1bmZvY3VzZWQifQ==',
        }

    def load_config(self) -> dict:
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            return {"use_proxies": False}
    
    def create_output_folder(self) -> str:
        output_path = "output"
        
        os.makedirs(output_path, exist_ok=True)
        
        for filename in ['trial.txt', 'invalid.txt', 'no_trial.txt', 'errors.txt', '1_month_trial.txt', '2_week_trial.txt', 'discount_tokens.txt']:
            open(os.path.join(output_path, filename), 'w').close()
            
        return output_path

    def load_tokens(self) -> None:
        try:
            with open('input/tokens.txt', 'r', encoding='utf-8') as file:
                tokens = file.read().strip().split('\n')
                token_count = len([t for t in tokens if t.strip()])
            self.console.success(f"Found tokens", str(token_count))
        except Exception as e:
            self.console.failed(f"Failed to count tokens", str(e))
    
    def get_next_token(self) -> Optional[str]:
        with self.file_lock:
            try:
                with open('input/tokens.txt', 'r', encoding='utf-8') as file:
                    lines = file.read().strip().split('\n')
                
                token_to_return = None
                remaining_tokens = []
                
                for line in lines:
                    if line.strip() and token_to_return is None:
                        token_to_return = line.strip()
                    elif line.strip():
                        remaining_tokens.append(line.strip())
                
                if token_to_return:
                    with open('input/tokens.txt', 'w', encoding='utf-8') as file:
                        file.write('\n'.join(remaining_tokens))
                
                return token_to_return
                    
            except Exception as e:
                self.console.warning("Failed to get next token", str(e))
                return None
    
    def remove_token_from_file(self, token_to_remove: str) -> None:
        pass

    def save_result_instantly(self, result_type: str, data: str) -> None:
        with self.file_lock:
            try:
                filename = {
                    'trial': 'trial.txt',
                    'invalid': 'invalid.txt', 
                    'no_trial': 'no_trial.txt',
                    'errors': 'errors.txt',
                    'one_month_trial': '1_month_trial.txt',
                    'two_week_trial': '2_week_trial.txt',
                    'discount_tokens': 'discount_tokens.txt'
                }.get(result_type)
                
                if filename:
                    filepath = os.path.join(self.output_folder, filename)
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(data + '\n')
            except Exception as e:
                self.console.warning(f"Failed to save {result_type}", str(e))
            
    def load_proxies(self) -> None:
        try:
            with open('input/proxies.txt', 'r', encoding='utf-8') as file:
                self.proxies = [proxy.strip() for proxy in file.read().strip().split('\n') if proxy.strip()]
            # self.console.success(f"Loaded proxies", str(len(self.proxies)))
        except Exception as e:
            self.console.failed(f"Failed to load proxies", str(e))
            self.proxies = []

    def get_random_proxy(self) -> Optional[str]:
        if self.proxies:
            return random.choice(self.proxies)
        return None

    def create_session(self, proxy: Optional[str] = None) -> Optional[tls_client.Session]:
        try:
            session = tls_client.Session(
                client_identifier="chrome124",
                random_tls_extension_order=True
            )
            
            if proxy:
                try:
                    auth_part, server_part = proxy.split('@')
                    username, password = auth_part.split(':')
                    host, port = server_part.split(':')
                    
                    session.proxies = {
                        'http': f'http://{username}:{password}@{host}:{port}',
                        'https': f'http://{username}:{password}@{host}:{port}'
                    }
                except Exception as e:
                    self.console.warning(f"Invalid proxy format", str(e))
                    
            return session
        except Exception as e:
            self.console.failed(f"Failed to create session", str(e))
            return None

    def check_trial(self, token_data: str) -> None:
        try:
            parts = token_data.split(':')
            if len(parts) != 3:
                self.console.failed("Invalid token format", token_data[:30] + "...")
                with self.lock:
                    self.results['errors'].append(token_data)
                self.save_result_instantly('errors', token_data)
                return
                
            email, password, token = parts
            
            proxy = self.get_random_proxy()
            
            session = self.create_session(proxy)
                
            if not session:
                self.console.failed("Session creation failed", email)
                with self.lock:
                    self.results['errors'].append(f"{token_data} | Session Error")
                self.save_result_instantly('errors', f"{token_data} | Session Error")
                return
            
            discount_found = False
            try:
                url_discount = "https://discord.com/api/v9/users/@me/billing/subscriptions/preview"
                headers_discount = {
                    'accept': '*/*',
                    'accept-language': 'en-US,en;q=0.9',
                    'authorization': token,
                    'content-type': 'application/json',
                    'cookie': '__dcfduid=48077eb0add711f0a00625a78a0a91ef; __sdcfduid=48077eb1add711f0a00625a78a0a91ef53510a13eac58a2a8944b9295fd9e64f344bca08b22bf1733ebcaddd95e94dea; _cfuvid=s9cZxNKL2A2hJYJiwjEBwEH0MvYu4z3MMKtUq.mRi7U-1760980058657-0.0.1.1-604800000; cf_clearance=LhOQjoj.elwmuGquaAin.90cuouhRrNLkdXeYm490OU-1760980065-1.2.1.1-z9AWmCiYEmWiCvdaP4m8JrrXSqjbZ.jPj4PwpyzMkKBv8e9fSLV8ots2OuAklm4hNQVmqm58q1CfFNSROt7iMhW_yTcOVLKvxw8Ri7SD9o6.XGRz3aYyb1ND6r4V3x0QgtCu8YoG.twdbFS1SZwK0ULC9lmoUsiEC42sePnsOibk5XfW8NqTA0AF.WHfRJKTGNrW2sIUe3h4kJU20sICe9k8tnukRXrCCFLuj6Xjcqw; locale=en-GB',
                    'origin': 'https://discord.com',
                    'priority': 'u=1, i',
                    'referer': 'https://discord.com/store',
                    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
                    'x-debug-options': 'bugReporterEnabled',
                    'x-discord-locale': 'en-GB',
                    'x-discord-timezone': 'Asia/Calcutta',
                    'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzE0MS4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTQxLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjQ1OTYzMSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6IjJhYjE2ZjhlLTY5ZTAtNDY4NS05NDBlLTE5MWVkNjI0MTZiNSIsImxhdW5jaF9zaWduYXR1cmUiOiI3ODMzY2EyMC0yMzgwLTQxYzYtOGM2Yy04M2I2Zjg0ODU3NjAiLCJjbGllbnRfYXBwX3N0YXRlIjoiZm9jdXNlZCIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6IjJkZGY0ZTQwLWQ2ZGItNGQ5Zi05ZWFjLTJjNTRkYTZiZjY3MiJ9'
                }
                data_discount = {
                    "items": [{"quantity": 1, "plan_id": "511651880837840896"}],
                    "payment_source_id": None,
                    "apply_entitlements": False,
                    "currency": "usd",
                    "renewal": True
                }
                response2 = session.post(url_discount, headers=headers_discount, json=data_discount)
                if response2.status_code == 200:
                    try:
                        data2 = response2.json()
                        if 'invoice_items' in data2 and isinstance(data2['invoice_items'], list):
                            for item in data2['invoice_items']:
                                if 'discounts' in item and isinstance(item['discounts'], list):
                                    for discount in item['discounts']:
                                        if (discount.get('type') == 1 and
                                            discount.get('percentage_amount') == 40 and
                                            discount.get('discount_id') == "1215366184820539392"):
                                            result = f"{email}:{password}:{token}"
                                            with self.lock:
                                                self.results['discount_tokens'].append(result)
                                            self.save_result_instantly('discount_tokens', result)
                                            self.console.discount("Discount Found", email)
                                            discount_found = True
                                            break
                                    else:
                                        continue
                                    break
                            else:
                                pass
                        else:
                            self.console.info("No invoice_items key or not list", f"for {email}")
                    except json.JSONDecodeError:
                        self.console.warning("Invalid JSON in discount response", email)
                else:
                    self.console.warning("Discount request failed", f"Status: {response2.status_code} for {email}")
            except Exception as e:
                self.console.failed("Discount check error", f"{str(e)} for {email}")
            
            headers = self.headers_template.copy()
            headers['authorization'] = token
            
            try:
                response = session.post(
                    self.url,
                    headers=headers,
                    json={}
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'message' in data and '404: Not Found' in data.get('message', '') and data.get('code') == 0:
                            result = f"{email}:{password}:{token}"
                            if not discount_found:
                                self.console.info("No trial available", email)
                                with self.lock:
                                    self.results['no_trial'].append(result)
                                self.save_result_instantly('no_trial', result)
                        elif 'user_trial_offer' in data and data.get('user_trial_offer') and 'trial_id' in data.get('user_trial_offer', {}):
                            trial_id = data['user_trial_offer']['trial_id']
                            expires_at = data['user_trial_offer'].get('expires_at', 'N/A')
                            result = f"{email}:{password}:{token}|{trial_id}"
                            
                            # Categorize trial based on starting digit
                            if trial_id.startswith('5'):
                                self.console.success("1 Month Trial found", f"{email} | ID: {trial_id} | Expires: {expires_at[:10]}")
                                with self.lock:
                                    self.results['one_month_trial'].append(result)
                                    self.results['trial'].append(result)  # Also save to main trial.txt
                                    self.trial_count += 1
                                    # If discount was also found, save to discount tokens too
                                    if discount_found:
                                        self.results['discount_tokens'].append(f"{email}:{password}:{token}") 
                                        self.save_result_instantly('discount_tokens', f"{email}:{password}:{token}")
                                self.save_result_instantly('one_month_trial', result)
                                self.save_result_instantly('trial', result)  # Also save to main trial.txt
                            elif trial_id.startswith('9'):
                                self.console.success("2 Week Trial found", f"{email} | ID: {trial_id} | Expires: {expires_at[:10]}")
                                with self.lock:
                                    self.results['two_week_trial'].append(result)
                                    self.results['trial'].append(result)  # Also save to main trial.txt
                                    self.trial_count += 1
                                    # If discount was also found, save to discount tokens too
                                    if discount_found:
                                        self.results['discount_tokens'].append(f"{email}:{password}:{token}")
                                        self.save_result_instantly('discount_tokens', f"{email}:{password}:{token}")
                                self.save_result_instantly('two_week_trial', result)
                                self.save_result_instantly('trial', result)  # Also save to main trial.txt
                            else:
                                self.console.success("Trial found", f"{email} | ID: {trial_id} | Expires: {expires_at[:10]}")
                                with self.lock:
                                    self.results['trial'].append(result)
                                    self.trial_count += 1
                                    # If discount was also found, save to discount tokens too
                                    if discount_found:
                                        self.results['discount_tokens'].append(f"{email}:{password}:{token}")
                                        self.save_result_instantly('discount_tokens', f"{email}:{password}:{token}")
                                self.save_result_instantly('trial', result)
                        else:
                            result = f"{email}:{password}:{token}"
                            if not discount_found:
                                self.console.info("No trial available", email)
                                with self.lock:
                                    self.results['no_trial'].append(result)
                                self.save_result_instantly('no_trial', result)
                    except json.JSONDecodeError:
                        self.console.warning("Invalid JSON response", email)
                        with self.lock:
                            self.results['errors'].append(f"{token_data} | Invalid JSON")
                        self.save_result_instantly('errors', f"{token_data} | Invalid JSON")
                            
                elif response.status_code == 401:
                    result = f"{email}:{password}:{token}"
                    self.console.failed("Invalid token", email)
                    with self.lock:
                        self.results['invalid'].append(result)
                    self.save_result_instantly('invalid', result)
                        
                elif response.status_code == 404:
                    result = f"{email}:{password}:{token}"
                    if not discount_found:
                        self.console.info("No trial available", email)
                        with self.lock:
                            self.results['no_trial'].append(result)
                        self.save_result_instantly('no_trial', result)
                        
                elif response.status_code == 405:
                    result = f"{email}:{password}:{token}"
                    if not discount_found:
                        self.console.info("No trial (405)", email)
                        with self.lock:
                            self.results['no_trial'].append(result)
                        self.save_result_instantly('no_trial', result)
                        
                elif response.status_code == 429:
                    self.console.warning("Rate limited", email)
                    with self.lock:
                        self.results['errors'].append(f"{token_data} | Rate Limited")
                    self.save_result_instantly('errors', f"{token_data} | Rate Limited")
                        
                else:
                    self.console.warning(f"HTTP {response.status_code}", email)
                    with self.lock:
                        self.results['errors'].append(f"{token_data} | HTTP {response.status_code}")
                    self.save_result_instantly('errors', f"{token_data} | HTTP {response.status_code}")
                        
            except Exception as tls_error:
                self.console.failed("TLS Client error", email)
                with self.lock:
                    self.results['errors'].append(f"{token_data} | TLS Error")
                self.save_result_instantly('errors', f"{token_data} | TLS Error")
                return
            except Exception as e:
                self.console.failed("Request failed", email)
                with self.lock:
                    self.results['errors'].append(f"{token_data} | Request Error")
                self.save_result_instantly('errors', f"{token_data} | Request Error")
                    
        except Exception as e:
            self.console.failed("Check failed", str(e)[:50])
            with self.lock:
                self.results['errors'].append(f"{token_data} | {str(e)}")
            self.save_result_instantly('errors', f"{token_data} | {str(e)}")
        
        finally:
            with self.lock:
                self.checked_count += 1
            if 'session' in locals() and session:
                try:
                    session.close()
                except:
                    pass

    def worker(self) -> None:
        while True:
            try:
                token_data = self.get_next_token()
                if not token_data:
                    break
                    
                self.check_trial(token_data)
                time.sleep(random.uniform(0.3, 0.8))
            except Exception as e:
                self.console.failed("Worker error", str(e))

    def save_results(self) -> None:
        self.console.info("Results saved to", self.output_folder)

    def display_stats(self) -> None:
        pass

    def run(self) -> None:
        # self.console.info("Discord Trial Checker", "Starting...")
        
        # self.console.info("Loading data", "Please wait...")
        self.load_tokens()
        self.load_proxies()
        
        try:
            with open('input/tokens.txt', 'r', encoding='utf-8') as file:
                if not file.read().strip():
                    self.console.failed("No tokens found", "Please add tokens to input/tokens.txt")
                    return
        except:
            self.console.failed("No tokens found", "Please add tokens to input/tokens.txt")
            return
        
        if not self.config.get('use_proxies', False):
            self.proxies = []
            self.console.info("Running without proxies", "Direct connection")
        else:
            self.console.info("Using proxies", f"{len(self.proxies)} proxies loaded")
        
        thread_input = self.console.input("Enter number of threads: ")
        try:
            self.thread_count = int(thread_input)
            if self.thread_count < 1:
                self.thread_count = 1
            elif self.thread_count > 100:
                self.thread_count = 100
                self.console.warning("Thread limit", "Maximum 100 threads")
        except ValueError:
            self.thread_count = 10
            self.console.warning("Invalid input", "Using default 10 threads")
        
        # self.console.info("Starting checker", f"{self.thread_count} threads")
        start_time = time.time()
        
        threads = []
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.worker, daemon=True)
            thread.start()
            threads.append(thread)
        
        try:
            while any(thread.is_alive() for thread in threads):
                if self.trial_count > 0:
                    with self.lock:
                        self.display_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            self.console.warning("Interrupted", "Saving results...")
        
        for thread in threads:
            thread.join(timeout=1)
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.console.success("CHECKING COMPLETED", f"Duration: {duration:.2f} seconds")
        self.console.info(f"Total Checked", str(self.checked_count))
        self.console.success(f"1 Month Trial", str(len(self.results['one_month_trial'])))
        self.console.success(f"Total Trial", str(self.trial_count))
        self.console.success(f"2 Week Trial", str(len(self.results['two_week_trial'])))
        self.console.discount(f"Discount Tokens", str(len(self.results['discount_tokens'])))
        self.console.warning(f"No Trial", str(len(self.results['no_trial'])))
        self.console.failed(f"Error", str(len(self.results['errors'])))
        self.console.failed(f"Invalid", str(len(self.results['invalid'])))
        
        self.save_results()
        
        self.console.success("All done!", f"Results in: {self.output_folder}")

def main():
    try:
        checker = DiscordTrialChecker()
        checker.run()
    except Exception as e:
        console = Console()
        console.failed("Fatal error", str(e))

if __name__ == "__main__":
    main()
