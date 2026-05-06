(base) peilongchencc@chenpeilongdeMacBook-Pro AlphaGBMskills % 使用 AlphaGBM 分析 AAPL 期权
zsh: command not found: 使用
(base) peilongchencc@chenpeilongdeMacBook-Pro AlphaGBMskills % claude
╭─── Claude Code v2.1.129 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                      │ Tips for getting started                                                                                     │
│             Welcome back!            │ Run /init to create a CLAUDE.md file with instructions for Claude                                            │
│                                      │ ──────────────────────────────────────────────────────────────────────────────────────────────────────────── │
│                ▐▛███▜▌               │ What's new                                                                                                   │
│               ▝▜█████▛▘              │ Added `--plugin-url <url>` flag to fetch a plugin `.zip` archive from a URL for the current session          │
│                 ▘▘ ▝▝                │ Added `CLAUDE_CODE_FORCE_SYNC_OUTPUT=1` env var to force-enable synchronized output on terminals that auto-… │
│                                      │ Added `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`: when set on Homebrew or WinGet installations, Claude Code … │
│   qwen3.6-plus · API Usage Billing   │ /release-notes for more                                                                                      │
│           ~/Desktop/AlphaGBMskills           │                                                                                                              │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

❯ 使用 AlphaGBM 分析 AAPL 期权                                                                                                                         

⏺ Let me first explore the AlphaGBM codebase to understand how to use it for AAPL options analysis.

⏺ Explore(Explore AlphaGBM codebase)
  ⎿  Done (27 tool uses · 66.9k tokens · 1m 42s)
  (ctrl+o to expand)

⏺ Good, I have a clear picture of the platform. Let me now read the AAPL mock data and invoke the relevant skills for a comprehensive options analysis.
                                                                                          
  Read 1 file (ctrl+o to expand)                                                                                                                       
                                                                                                                                                       
⏺ Now I have all the data. Let me read the key SKILL.md files to apply the proper analysis framework.                                                  
                                                                                                                                                       
  Read 4 files (ctrl+o to expand)                                                                                                                      
                                                                                                                                                       
⏺ Let me find the actual skill file locations.                                                                                                         
                                                                                                                                                       
  Searched for 1 pattern, read 4 files (ctrl+o to expand)                                                                                              
                                                                                                                                                       
⏺ Now I have all the data and the analysis framework. Here is the comprehensive AAPL Options Analysis using AlphaGBM:                                  
                                                                                                                                                       
  ---                                                                                                                                                  
  AlphaGBM: AAPL Options Analysis                                                                                                                      
                                                                                                                                                       
  Data Date: 2026-04-09 | Underlying Price: $261.40 (-0.8%)                                                                                            
                                                                                                                                                       
  ---             
  1. Stock Overview & GBM Signal                                                                                                                       
                                                                                                                                                       
  ┌───────────┬───────────────────┬─────────────┬─────────┐
  │  Metric   │       Value       │   Metric    │  Value  │                                                                                            
  ├───────────┼───────────────────┼─────────────┼─────────┤                                                                                            
  │ Price     │ $261.40           │ Market Cap  │ $3.92T  │                                                                                            
  ├───────────┼───────────────────┼─────────────┼─────────┤                                                                                            
  │ P/E       │ 32.5x             │ Forward P/E │ 28.8x   │                                                                                            
  ├───────────┼───────────────────┼─────────────┼─────────┤                                                                                            
  │ RSI(14)   │ 48.2              │ Beta        │ 1.18    │                                                                                            
  ├───────────┼───────────────────┼─────────────┼─────────┤                                                                                            
  │ SMA 50    │ $272.80           │ SMA 200     │ $238.50 │
  ├───────────┼───────────────────┼─────────────┼─────────┤                                                                                            
  │ 52W Range │ $186.40 - $282.50 │ Div Yield   │ 0.42%   │
  └───────────┴───────────────────┴─────────────┴─────────┘                                                                                            
                  
  GBM Overall Score: 7.0/10 — Moderately Bullish                                                                                                       
                  
  ┌─────────────┬───────┬─────────────────────────────────────────────────────────────────────┐                                                        
  │   Pillar    │ Score │                               Summary                               │
  ├─────────────┼───────┼─────────────────────────────────────────────────────────────────────┤                                                        
  │ Fundamental │ 7.8   │ Services +15% YoY, iPhone stable, forward PE 28.8x fair for quality │
  ├─────────────┼───────┼─────────────────────────────────────────────────────────────────────┤                                                        
  │ Technical   │ 5.5   │ Below 50 SMA ($273), MACD bearish, RSI 48 neutral                   │                                                        
  ├─────────────┼───────┼─────────────────────────────────────────────────────────────────────┤                                                        
  │ Sentiment   │ 6.8   │ Put/Call 0.82 mildly bullish, IV Rank 58 moderate                   │                                                        
  ├─────────────┼───────┼─────────────────────────────────────────────────────────────────────┤                                                        
  │ Flow        │ 7.5   │ Institutional call buying in May, smart money accumulating          │
  ├─────────────┼───────┼─────────────────────────────────────────────────────────────────────┤                                                        
  │ Valuation   │ 7.5   │ 7.5% below 52W high, PEG 2.1 rich but justified                     │
  └─────────────┴───────┴─────────────────────────────────────────────────────────────────────┘                                                        
                  
  Target Prices: Bull $290 | Base $275 | Bear $235                                                                                                     
                  
  ---                                                                                                                                                  
  2. Options Overview — IV & VRP
                                                                                                                                                       
  ┌────────────────┬───────┬───────────────────────────────────────┐
  │     Metric     │ Value │            Interpretation             │                                                                                   
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ IV 30d         │ 32.5% │ Above HV — options are priced rich    │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ IV 60d         │ 30.2% │ Term structure upward sloping         │                                                                                   
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ IV 90d         │ 28.8% │ Back-month IV declining               │                                                                                   
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ HV 20d         │ 28.5% │ Recent realized vol                   │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ HV 60d         │ 25.8% │ 60-day realized vol                   │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ VRP            │ +4.0% │ Normal range — slight edge to sellers │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ IV Rank        │ 58    │ Moderate — not extreme                │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ IV Percentile  │ 52    │ Slightly above median                 │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ Put/Call Ratio │ 0.82  │ Mildly bullish (more call activity)   │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ Put OI         │ 4.18M │ —                                     │
  ├────────────────┼───────┼───────────────────────────────────────┤                                                                                   
  │ Call OI        │ 5.10M │ —                                     │
  └────────────────┴───────┴───────────────────────────────────────┘                                                                                   
                  
  VRP Assessment: +4.0% is in the "normal" band (±5%). Neither strongly favors buying nor selling — slight edge to premium sellers.                    
                  
  ---                                                                                                                                                  
  3. Term Structure — Backwardation (Earnings Effect)
                                                                                                                                                       
  ┌────────────┬─────┬────────┬─────────────────────────────┐
  │   Expiry   │ DTE │ ATM IV │           Signal            │                                                                                          
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-04-17 │ 8   │ 36.8%  │ Front-month elevated        │                                                                                          
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-04-25 │ 16  │ 35.2%  │ Still elevated              │                                                                                          
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-05-02 │ 23  │ 38.5%  │ Peak — earnings week 05/01  │                                                                                          
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-05-16 │ 37  │ 32.0%  │ Post-earnings normalization │
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-06-20 │ 72  │ 29.8%  │ Back to normal              │
  ├────────────┼─────┼────────┼─────────────────────────────┤                                                                                          
  │ 2026-09-18 │ 162 │ 28.2%  │ Long-term baseline          │
  └────────────┴─────┴────────┴─────────────────────────────┘                                                                                          
                  
  Shape: Event-Driven Backwardation — the 05/02 expiry shows a massive IV spike (38.5%) due to earnings on 05/01. This creates a clear "earnings kink" 
  in the term structure.
                                                                                                                                                       
  ---                                                                                                                                                  
  4. Volatility Surface Analysis
                                                                                                                                                       
  2026-04-25 Expiry (16 DTE)
                                                                                                                                                       
  ┌────────┬───────────┬─────────┬────────┬──────┐                                                                                                     
  │ Strike │ Moneyness │ Call IV │ Put IV │ Skew │                                                                                                     
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 240    │ 0.918     │ 40.5%   │ 41.8%  │ +1.3 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 250    │ 0.956     │ 37.2%   │ 38.2%  │ +1.0 │                                                                                                     
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 255    │ 0.976     │ 35.8%   │ 36.5%  │ +0.7 │                                                                                                     
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 260    │ 0.995     │ 35.2%   │ 35.6%  │ +0.4 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 265    │ 1.014     │ 35.5%   │ 36.0%  │ +0.5 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 270    │ 1.033     │ 36.2%   │ 36.8%  │ +0.6 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 280    │ 1.071     │ 38.0%   │ 38.8%  │ +0.8 │
  └────────┴───────────┴─────────┴────────┴──────┘                                                                                                     
                  
  2026-05-16 Expiry (37 DTE)                                                                                                                           
                  
  ┌────────┬───────────┬─────────┬────────┬──────┐                                                                                                     
  │ Strike │ Moneyness │ Call IV │ Put IV │ Skew │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 240    │ 0.918     │ 35.8%   │ 37.0%  │ +1.2 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 250    │ 0.956     │ 33.2%   │ 34.0%  │ +0.8 │                                                                                                     
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 255    │ 0.976     │ 32.2%   │ 32.8%  │ +0.6 │                                                                                                     
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 260    │ 0.995     │ 32.0%   │ 32.4%  │ +0.4 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 265    │ 1.014     │ 32.2%   │ 32.8%  │ +0.6 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 270    │ 1.033     │ 32.8%   │ 33.5%  │ +0.7 │
  ├────────┼───────────┼─────────┼────────┼──────┤                                                                                                     
  │ 280    │ 1.071     │ 34.2%   │ 35.0%  │ +0.8 │
  └────────┴───────────┴─────────┴────────┴──────┘                                                                                                     
                  
  Key observations:                                                                                                                                    
  - Skew: Both expiries show a classic "smile" with elevated wings — OTM puts slightly higher IV than OTM calls, indicating mild put-side hedging
  demand                                                                                                                                               
  - 25d skew: -3.5% overall — not extreme, market not pricing severe tail risk
  - Relative IV: May-16 IV is ~3pp lower than Apr-25 at ATM, reflecting post-earnings normalization                                                    
                                                                                                                                                       
  ---                                                                                                                                                  
  5. Scored Options Contracts (from mock data chain)                                                                                                   
                                                                                                                                                       
  Top Pick: AAPL 04/25 $265 Call — Score 8.0/10
                                                                                                                                                       
  ┌───────────────────┬───────┐                                                                                                                        
  │      Factor       │ Score │                                                                                                                        
  ├───────────────────┼───────┤                                                                                                                        
  │ Liquidity         │ 9.0   │
  ├───────────────────┼───────┤                                                                                                                        
  │ IV Attractiveness │ 7.0   │                                                                                                                        
  ├───────────────────┼───────┤                                                                                                                        
  │ Greeks Balance    │ 8.0   │                                                                                                                        
  ├───────────────────┼───────┤                                                                                                                        
  │ Risk/Reward       │ 8.0   │
  └───────────────────┴───────┘                                                                                                                        
                  
  - Bid/Ask: $7.20 / $7.50 | Volume: 18,500 | OI: 52,000                                                                                               
  - Delta: 0.46 | Gamma: 0.022 | Theta: -0.22 | Vega: 0.28
  - Near-ATM, high liquidity, good Greek balance                                                                                                       
                                                                                                                                                       
  Second Pick: AAPL 04/25 $255 Put — Score 7.5/10                                                                                                      
                                                                                                                                                       
  ┌───────────────────┬───────┐                                                                                                                        
  │      Factor       │ Score │
  ├───────────────────┼───────┤                                                                                                                        
  │ Liquidity         │ 8.5   │
  ├───────────────────┼───────┤                                                                                                                        
  │ IV Attractiveness │ 7.0   │                                                                                                                        
  ├───────────────────┼───────┤                                                                                                                        
  │ Greeks Balance    │ 7.5   │                                                                                                                        
  ├───────────────────┼───────┤                                                                                                                        
  │ Risk/Reward       │ 7.0   │
  └───────────────────┴───────┘                                                                                                                        
                  
  - Bid/Ask: $5.80 / $6.10 | Volume: 14,200 | OI: 45,000                                                                                               
  - Delta: -0.38 | Gamma: 0.020 | Theta: -0.20 | Vega: 0.26
  - Good hedge candidate, below current price                                                                                                          
                                                                                                                                                       
  ---                                                                                                                                                  
  6. Earnings Analysis (05/01 — 22 Days Away)                                                                                                          
                                                                                                                                                       
  Historical IV Crush
                                                                                                                                                       
  ┌───────────────┬───────────┬──────────┬─────────┬─────────────┬──────────────┐                                                                      
  │ Earnings Date │ IV Before │ IV After │ Crush % │ Actual Move │ Implied Move │                                                                      
  ├───────────────┼───────────┼──────────┼─────────┼─────────────┼──────────────┤                                                                      
  │ 2026-01-30    │ 42.5%     │ 28.2%    │ 33.6%   │ -3.2%       │ ±4.5%        │
  ├───────────────┼───────────┼──────────┼─────────┼─────────────┼──────────────┤                                                                      
  │ 2025-10-30    │ 38.2%     │ 26.5%    │ 30.6%   │ +2.1%       │ ±3.8%        │                                                                      
  ├───────────────┼───────────┼──────────┼─────────┼─────────────┼──────────────┤                                                                      
  │ 2025-07-31    │ 35.8%     │ 25.2%    │ 29.6%   │ -1.5%       │ ±3.5%        │                                                                      
  ├───────────────┼───────────┼──────────┼─────────┼─────────────┼──────────────┤                                                                      
  │ 2025-04-24    │ 40.1%     │ 27.8%    │ 30.7%   │ +5.2%       │ ±4.0%        │
  └───────────────┴───────────┴──────────┴─────────┴─────────────┴──────────────┘                                                                      
                  
  Average IV Crush: ~31.1% | Avg Actual Move: ~3.0%                                                                                                    
                  
  Implication: IV consistently crushes ~31% post-earnings. The May-02 expiry ATM IV at 38.5% will likely drop to ~26-27% after the announcement. Naked 
  long options before earnings are a losing strategy — you need the move to exceed the implied move AND overcome the IV crush.
                                                                                                                                                       
  ---                                                                                                                                                  
  7. Recommended Strategies
                                                                                                                                                       
  Strategy 1: Bull Call Spread (Score: 7.5/10) — Directional Play
                                                                                                                                                       
  ┌───────┬──────┬────────┬────────┬───────┐                                                                                                           
  │  Leg  │ Type │ Strike │ Action │ Price │                                                                                                           
  ├───────┼──────┼────────┼────────┼───────┤                                                                                                           
  │ Long  │ Call │ 265    │ Buy    │ $7.35 │
  ├───────┼──────┼────────┼────────┼───────┤                                                                                                           
  │ Short │ Call │ 280    │ Sell   │ $3.20 │                                                                                                           
  └───────┴──────┴────────┴────────┴───────┘                                                                                                           
                                                                                                                                                       
  - Net Debit: $4.15 ($415/contract)                                                                                                                   
  - Max Profit: $10.85 ($1,085/contract)
  - Max Loss: $4.15 ($415/contract)                                                                                                                    
  - Breakeven: $269.15                                                                                                                                 
  - Probability of Profit: 44.5%                                                                                                                       
  - Risk/Reward Ratio: 2.61                                                                                                                            
                                                                                                                                                       
  Why it works: Caps risk while maintaining upside to $280 (base target $275 is close). Short leg partially offsets IV crush.                          
                                                                                                                                                       
  Strategy 2: Cash-Secured Put (Score: 8.0/10) — Income Play                                                                                           
                  
  ┌───────┬──────┬────────┬────────┬───────┐                                                                                                           
  │  Leg  │ Type │ Strike │ Action │ Price │
  ├───────┼──────┼────────┼────────┼───────┤                                                                                                           
  │ Short │ Put  │ 250    │ Sell   │ $4.50 │
  └───────┴──────┴────────┴────────┴───────┘                                                                                                           
                                                                                                                                                       
  - Premium: $450/contract                                                                                                                             
  - Max Profit: $450 (premium)                                                                                                                         
  - Max Loss: $24,550 (if assigned at $250)                                                                                                            
  - Breakeven: $245.50                                                                                                                                 
  - Probability of Profit: 68.2%                                                                                                                       
  - Capital Required: ~$25,000 (cash-secured)                                                                                                          
                                                                                                                                                       
  Why it works: $250 is below SMA 200 ($238.50 is further support) and aligns with bear target $235 buffer. High POP of 68.2%. The recommended strategy
   from GBM analysis.                                                                                                                                  
                                                                                                                                                       
  ---                                                                                                                                                  
  8. Unusual Activity
                                                                                                                                                       
  ┌───────┬──────┬────────┬────────┬────────┬────────┬────────┬─────────┬───────────────┐
  │ Date  │ Type │ Strike │ Expiry │ Volume │   OI   │ Vol/OI │ Premium │   Sentiment   │                                                              
  ├───────┼──────┼────────┼────────┼────────┼────────┼────────┼─────────┼───────────────┤                                                              
  │ 04/09 │ Call │ 280    │ 05/16  │ 42,000 │ 12,500 │ 3.36x  │ $3.36M  │ Bullish       │                                                              
  ├───────┼──────┼────────┼────────┼────────┼────────┼────────┼─────────┼───────────────┤                                                              
  │ 04/08 │ Put  │ 245    │ 04/25  │ 32,000 │ 9,800  │ 3.27x  │ $0.96M  │ Bearish Hedge │                                                              
  └───────┴──────┴────────┴────────┴────────┴────────┴────────┴─────────┴───────────────┘                                                              
                                                                                                                                                       
  Read: Smart money is buying $280 calls for May (bullish bet on post-earnings recovery) while simultaneously hedging with $245 puts for April         
  (downside protection). This is a classic "buy calls, hedge with cheap puts" institutional flow.
                                                                                                                                                       
  ---                                                                                                                                                  
  9. Market Sentiment Context
                                                                                                                                                       
  ┌─────────────────┬────────────┬────────────────────────────────────────────┐
  │     Metric      │   Value    │               Interpretation               │                                                                        
  ├─────────────────┼────────────┼────────────────────────────────────────────┤                                                                        
  │ VIX             │ 22.8       │ 62nd percentile — elevated but not extreme │                                                                        
  ├─────────────────┼────────────┼────────────────────────────────────────────┤                                                                        
  │ Fear & Greed    │ 38 (Fear)  │ Cautious environment                       │                                                                        
  ├─────────────────┼────────────┼────────────────────────────────────────────┤                                                                        
  │ SPY Put/Call    │ 1.05       │ Slightly defensive market                  │                                                                        
  ├─────────────────┼────────────┼────────────────────────────────────────────┤                                                                        
  │ Sector Rotation │ Late Cycle │ Quality favored                            │
  └─────────────────┴────────────┴────────────────────────────────────────────┘                                                                        
                  
  ---                                                                                                                                                  
  10. Risk Factors
                                                                                                                                                       
  1. Earnings in 22 days — IV will remain elevated, then crush ~31% post-announcement
  2. Trade policy / tariff exposure — AAPL has supply chain sensitivity                                                                                
  3. Below 50-day SMA ($272.80) — technical resistance overhead                                                                                        
  4. Pre-earnings IV buildup makes naked calls expensive — spreads strongly preferred                                                                  
                                                                                                                                                       
  ---                                                                                                                                                  
  Summary & Action Plan                                                                                                                                
                                                                                                                                                       
  ┌──────────────────────────┬─────────────────────────────────────────────────────────┬────────────────────────────────────────────────────────┐
  │         Scenario         │                    Recommended Trade                    │                       Rationale                        │      
  ├──────────────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤      
  │ Bullish on AAPL          │ Bull Call Spread 265/280 (May or Apr)                   │ Defined risk, mitigates IV crush, 2.6:1 R/R            │      
  ├──────────────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤      
  │ Income generation        │ Cash-Secured Put $250                                   │ 68.2% POP, $250 is strong support level                │      
  ├──────────────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤      
  │ Hedging existing long    │ Buy Apr-25 $255 Put                                     │ Score 7.5/10, cost ~$595/contract, delta hedge         │      
  ├──────────────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤      
  │ Pre-earnings speculation │ Avoid naked longs                                       │ Historical 31% IV crush overwhelms most long positions │
  ├──────────────────────────┼─────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤      
  │ Post-earnings play       │ Wait for IV crush, then buy long-dated calls if bullish │ IV drops from ~38% to ~27%, cheaper entry              │
  └──────────────────────────┴─────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘      
                  
  Best overall trade: Cash-Secured Put at $250 — highest score (8.0), highest POP (68.2%), aligns with GBM's "quality compounder on pullback" thesis.  
                  
✻ Baked for 3m 33s
                                                                                          
❯ 请使用中文为我详细解释一下。                                                                                                                         
                                                                                                                                                       
⏺ AlphaGBM：AAPL 期权深度分析                                                                                                                          
                                                                                                                                                       
  数据日期： 2026-04-09 | 标的价格： $261.40（当日下跌 0.8%）                                                                                          
                                                                                                                                                       
  ---                                                                                                                                                  
  一、股票基本面概览                                                                                                                                   
                                                                                                                                                       
  ┌────────────┬──────────────┬──────────────────────────────┐
  │    指标    │     数值     │             含义             │                                                                                         
  ├────────────┼──────────────┼──────────────────────────────┤
  │ 当前价格   │ $261.40      │ 从52周高点$282.50回调约7.5%  │                                                                                         
  ├────────────┼──────────────┼──────────────────────────────┤
  │ 市值       │ 3.92万亿美元 │ 全球最大上市公司             │                                                                                         
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ 市盈率 P/E │ 32.5x        │ 估值偏高，但对质量股合理     │                                                                                         
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ 远期市盈率 │ 28.8x        │ 市场预期盈利增长             │
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ RSI(14)    │ 48.2         │ 中性区域，无超买超卖         │
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ Beta       │ 1.18         │ 波动略大于大盘               │
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ 50日均线   │ $272.80      │ 股价在其下方，短期偏弱       │
  ├────────────┼──────────────┼──────────────────────────────┤                                                                                         
  │ 200日均线  │ $238.50      │ 股价在其上方，长期趋势仍向上 │
  └────────────┴──────────────┴──────────────────────────────┘                                                                                         
                  
  GBM综合评分：7.0/10 — 温和看多                                                                                                                       
                  
  ┌──────────┬──────┬───────────────────────────────────────────────────┐                                                                              
  │   维度   │ 评分 │                       解读                        │
  ├──────────┼──────┼───────────────────────────────────────────────────┤                                                                              
  │ 基本面   │ 7.8  │ 服务收入同比增长15%，iPhone销售稳定               │
  ├──────────┼──────┼───────────────────────────────────────────────────┤                                                                              
  │ 技术面   │ 5.5  │ 低于50日均线，MACD看跌，RSI中性                   │                                                                              
  ├──────────┼──────┼───────────────────────────────────────────────────┤                                                                              
  │ 情绪面   │ 6.8  │ 看跌/看涨比0.82偏多，IV排名58中等                 │                                                                              
  ├──────────┼──────┼───────────────────────────────────────────────────┤                                                                              
  │ 资金流向 │ 7.5  │ 机构在五月合约上买入看涨期权                      │
  ├──────────┼──────┼───────────────────────────────────────────────────┤                                                                              
  │ 估值     │ 7.5  │ 距52周高点有7.5%空间，PEG 2.1虽贵但有资本回报支撑 │
  └──────────┴──────┴───────────────────────────────────────────────────┘                                                                              
                  
  目标价： 乐观 $290 | 基准 $275 | 悲观 $235                                                                                                           
                  
  ---                                                                                                                                                  
  二、期权核心指标 — 隐含波动率与波动率风险溢价
                                                                                                                                                       
  ┌────────────────────┬─────────┬──────────────────────────┐
  │        指标        │  数值   │           含义           │                                                                                          
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 30天隐含波动率(IV) │ 32.5%   │ 高于实际波动率，期权偏贵 │                                                                                          
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 60天IV             │ 30.2%   │ 期限结构上倾             │                                                                                          
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 90天IV             │ 28.8%   │ 远月IV递减               │                                                                                          
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 20天历史波动率(HV) │ 28.5%   │ 近期实际波动幅度         │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 60天HV             │ 25.8%   │ 60天实际波动             │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ VRP                │ +4.0%   │ 正常区间，卖方略有优势   │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ IV排名             │ 58      │ 中等水平，不极端         │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ IV百分位           │ 52      │ 略高于中位数             │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 看跌/看涨比        │ 0.82    │ 看涨期权更活跃，偏多信号 │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 看涨未平仓         │ 510万张 │ —                        │
  ├────────────────────┼─────────┼──────────────────────────┤                                                                                          
  │ 看跌未平仓         │ 418万张 │ —                        │
  └────────────────────┴─────────┴──────────────────────────┘                                                                                          
                  
  VRP（波动率风险溢价）解读： VRP = IV - HV = +4.0%。这个值在正常区间（±5%），没有明显偏向。正值意味着隐含波动率略高于实际波动率，期权卖方有小幅优势。 
                  
  VRP参考标准：                                                                                                                                        
                  
  ┌──────────┬──────────┬────────┐                                                                                                                     
  │ VRP水平  │  对卖方  │ 对买方 │
  ├──────────┼──────────┼────────┤                                                                                                                     
  │ ≥15%     │ 非常有利 │ 不利   │
  ├──────────┼──────────┼────────┤                                                                                                                     
  │ 5-15%    │ 有利     │ 略不利 │                                                                                                                     
  ├──────────┼──────────┼────────┤                                                                                                                     
  │ ±5%      │ 中性     │ 中性   │                                                                                                                     
  ├──────────┼──────────┼────────┤                                                                                                                     
  │ -15%~-5% │ 不利     │ 有利   │
  └──────────┴──────────┴────────┘                                                                                                                     
                  
  当前+4.0%接近中性，卖方略有优势但不明显。                                                                                                            
                  
  ---                                                                                                                                                  
  三、期限结构 — 财报导致的反向期限结构
                                                                                                                                                       
  ┌────────┬──────────┬───────────────┬────────────────────────┐
  │ 到期日 │ 距今天数 │ ATM隐含波动率 │          信号          │                                                                                       
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 04/17  │ 8天      │ 36.8%         │ 近月偏高               │                                                                                       
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 04/25  │ 16天     │ 35.2%         │ 仍偏高                 │                                                                                       
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 05/02  │ 23天     │ 38.5%         │ 峰值 — 财报周（05/01） │                                                                                       
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 05/16  │ 37天     │ 32.0%         │ 财报后回归正常         │
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 06/20  │ 72天     │ 29.8%         │ 回到正常水平           │
  ├────────┼──────────┼───────────────┼────────────────────────┤                                                                                       
  │ 09/18  │ 162天    │ 28.2%         │ 长期基准线             │
  └────────┴──────────┴───────────────┴────────────────────────┘                                                                                       
                  
  关键发现：                                                                                                                                           
                  
  这是一个典型的**"事件驱动型反向期限结构"**（Event-Driven                                                                                             
  Backwardation）。正常情况下，期限越长IV越高（contango/正向结构），但这里5月2日的IV飙升至38.5%，因为苹果财报将在5月1日公布。这意味着：
                                                                                                                                                       
  1. 短期期权非常贵 — 市场在为财报定价                                                                                                                 
  2. 财报后IV会暴跌 — 历史上平均暴跌约31%
  3. 财报前买入裸期权是亏钱策略 — IV暴跌会吞噬期权价值                                                                                                 
                                                                                                                                                       
  ---                                                                                                                                                  
  四、波动率曲面分析                                                                                                                                   
                                                                                                                                                       
  波动率曲面展示了不同行权价和到期日的IV分布。
                                                                                                                                                       
  4月25日到期（距16天）                                                                                                                                
                                                                                                                                                       
  ┌────────┬─────────────┬────────┬────────┬──────┐                                                                                                    
  │ 行权价 │  价内程度   │ 看涨IV │ 看跌IV │ 偏斜 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 240    │ 深度OTM看跌 │ 40.5%  │ 41.8%  │ +1.3 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 250    │ OTM看跌     │ 37.2%  │ 38.2%  │ +1.0 │                                                                                                    
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 255    │ 轻度OTM看跌 │ 35.8%  │ 36.5%  │ +0.7 │                                                                                                    
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 260    │ 近ATM       │ 35.2%  │ 35.6%  │ +0.4 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 265    │ 轻度OTM看涨 │ 35.5%  │ 36.0%  │ +0.5 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 270    │ OTM看涨     │ 36.2%  │ 36.8%  │ +0.6 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 280    │ 深度OTM看涨 │ 38.0%  │ 38.8%  │ +0.8 │
  └────────┴─────────────┴────────┴────────┴──────┘                                                                                                    
                  
  5月16日到期（距37天）                                                                                                                                
                  
  ┌────────┬─────────────┬────────┬────────┬──────┐                                                                                                    
  │ 行权价 │  价内程度   │ 看涨IV │ 看跌IV │ 偏斜 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 240    │ 深度OTM看跌 │ 35.8%  │ 37.0%  │ +1.2 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 250    │ OTM看跌     │ 33.2%  │ 34.0%  │ +0.8 │                                                                                                    
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 255    │ 轻度OTM看跌 │ 32.2%  │ 32.8%  │ +0.6 │                                                                                                    
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 260    │ 近ATM       │ 32.0%  │ 32.4%  │ +0.4 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 265    │ 轻度OTM看涨 │ 32.2%  │ 32.8%  │ +0.6 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 270    │ OTM看涨     │ 32.8%  │ 33.5%  │ +0.7 │
  ├────────┼─────────────┼────────┼────────┼──────┤                                                                                                    
  │ 280    │ 深度OTM看涨 │ 34.2%  │ 35.0%  │ +0.8 │
  └────────┴─────────────┴────────┴────────┴──────┘                                                                                                    
                  
  核心观察：                                                                                                                                           
                  
  1. "微笑"形态：两端的IV都高于中间，这是期权市场的经典形态 — 市场对极端波动（大涨或大跌）的定价更高                                                   
  2. 看跌偏斜：OTM看跌期权的IV略高于对应行权价的看涨期权，说明市场有一定对冲需求
  3. 25日偏斜 -3.5%：不算极端，市场没有定价严重的尾部风险                                                                                              
  4. 5月16日IV比4月25日低约3个百分点：反映了财报后波动率回归正常                                                                                       
                                                                                                                                                       
  ---                                                                                                                                                  
  五、评分最高的期权合约                                                                                                                               
                                                                                                                                                       
  第一名：AAPL 4/25 $265 看涨期权 — 评分 8.0/10
                                                                                                                                                       
  ┌──────────────┬────────────┐                                                                                                                        
  │     因素     │    评分    │                                                                                                                        
  ├──────────────┼────────────┤                                                                                                                        
  │ 流动性       │ 9.0 — 极佳 │
  ├──────────────┼────────────┤                                                                                                                        
  │ IV吸引力     │ 7.0 — 中等 │                                                                                                                        
  ├──────────────┼────────────┤                                                                                                                        
  │ 希腊字母平衡 │ 8.0 — 良好 │                                                                                                                        
  ├──────────────┼────────────┤                                                                                                                        
  │ 风险回报     │ 8.0 — 良好 │
  └──────────────┴────────────┘                                                                                                                        
                  
  - 买卖价：$7.20 / $7.50                                                                                                                              
  - 成交量：18,500张 | 未平仓：52,000张
  - Delta：0.46（股价每涨$1，期权约涨$0.46）                                                                                                           
  - Gamma：0.022（Delta的加速度）                                                                                                                      
  - Theta：-0.22（每天时间损耗约$0.22/股）                                                                                                             
  - Vega：0.28（IV每降1%，期权跌约$0.28/股）                                                                                                           
                                                                                                                                                       
  评价： 近ATM（价内程度0.995），流动性极好，希腊字母平衡。适合作为看涨方向性交易的标的。                                                              
                                                                                                                                                       
  第二名：AAPL 4/25 $255 看跌期权 — 评分 7.5/10                                                                                                        
                  
  ┌──────────────┬──────┐                                                                                                                              
  │     因素     │ 评分 │
  ├──────────────┼──────┤                                                                                                                              
  │ 流动性       │ 8.5  │
  ├──────────────┼──────┤                                                                                                                              
  │ IV吸引力     │ 7.0  │                                                                                                                              
  ├──────────────┼──────┤                                                                                                                              
  │ 希腊字母平衡 │ 7.5  │                                                                                                                              
  ├──────────────┼──────┤                                                                                                                              
  │ 风险回报     │ 7.0  │
  └──────────────┴──────┘                                                                                                                              
                  
  - 买卖价：$5.80 / $6.10                                                                                                                              
  - 成交量：14,200张 | 未平仓：45,000张
  - Delta：-0.38                                                                                                                                       
  - 适合作为对冲工具                                                                                                                                   
                                                                                                                                                       
  ---                                                                                                                                                  
  六、财报分析（05/01 — 距今22天）                                                                                                                     
                                                                                                                                                       
  历史IV暴跌数据  
                                                                                                                                                       
  ┌────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐                                                                                
  │  财报日期  │ 财报前IV │ 财报后IV │ 暴跌幅度 │ 实际波动 │ 预期波动 │                                                                                
  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤                                                                                
  │ 2026-01-30 │ 42.5%    │ 28.2%    │ 33.6%    │ -3.2%    │ ±4.5%    │
  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤                                                                                
  │ 2025-10-30 │ 38.2%    │ 26.5%    │ 30.6%    │ +2.1%    │ ±3.8%    │                                                                                
  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤                                                                                
  │ 2025-07-31 │ 35.8%    │ 25.2%    │ 29.6%    │ -1.5%    │ ±3.5%    │                                                                                
  ├────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤                                                                                
  │ 2025-04-24 │ 40.1%    │ 27.8%    │ 30.7%    │ +5.2%    │ ±4.0%    │
  └────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘                                                                                
                  
  平均IV暴跌幅度：约31.1% | 平均实际波动：约3.0%                                                                                                       
                  
  关键启示：                                                                                                                                           
                  
  苹果财报后IV平均暴跌31%，这是一个非常稳定且可预测的模式。05/02到期的ATM IV目前为38.5%，财报后大概率跌至26-27%左右。                                  
                  
  这意味着什么？                                                                                                                                       
                  
  - 如果你在财报前买入裸看涨/看跌期权，你需要股价波动超过预期波动（±4%左右）AND同时克服IV暴跌带来的期权贬值。这在历史上很少发生（平均实际波动只有3%）。
  - 财报前裸买期权 = 输钱策略。 应该用价差策略（spread）来对冲IV风险。
                                                                                                                                                       
  ---                                                                                                                                                  
  七、推荐策略                                                                                                                                         
                                                                                                                                                       
  策略一：牛市看涨价差（Bull Call Spread）— 评分 7.5/10
                                                                                                                                                       
  ┌──────┬──────┬────────┬──────┬───────┐                                                                                                              
  │  腿  │ 类型 │ 行权价 │ 操作 │ 价格  │                                                                                                              
  ├──────┼──────┼────────┼──────┼───────┤                                                                                                              
  │ 买入 │ 看涨 │ 265    │ Buy  │ $7.35 │
  ├──────┼──────┼────────┼──────┼───────┤                                                                                                              
  │ 卖出 │ 看涨 │ 280    │ Sell │ $3.20 │                                                                                                              
  └──────┴──────┴────────┴──────┴───────┘                                                                                                              
                                                                                                                                                       
  - 净支出（debit）： $4.15（每张合约$415）                                                                                                            
  - 最大利润： $10.85（每张$1,085）
  - 最大亏损： $4.15（每张$415）                                                                                                                       
  - 盈亏平衡点： $269.15                                                                                                                               
  - 获利概率： 44.5%                                                                                                                                   
  - 风险回报比： 2.61:1                                                                                                                                
                                                                                                                                                       
  为什么有效：                                                                                                                                         
                                                                                                                                                       
  1. 买入265看涨 + 卖出280看涨，锁定风险也锁定利润                                                                                                     
  2. 卖出的280看涨部分抵消了IV暴跌的影响（双腿的IV变化互相抵消一部分）
  3. 基准目标价$275在价差范围内，有合理的获利空间                                                                                                      
  4. 风险回报比2.61:1很优秀 — 每承担$1风险，潜在回报$2.61                                                                                              
                                                                                                                                                       
  策略二：现金担保看跌期权（Cash-Secured Put）— 评分 8.0/10                                                                                            
                                                                                                                                                       
  ┌──────┬──────┬────────┬──────┬───────┐                                                                                                              
  │  腿  │ 类型 │ 行权价 │ 操作 │ 价格  │
  ├──────┼──────┼────────┼──────┼───────┤                                                                                                              
  │ 卖出 │ 看跌 │ 250    │ Sell │ $4.50 │
  └──────┴──────┴────────┴──────┴───────┘                                                                                                              
                                                                                                                                                       
  - 收取权利金： $450/张
  - 最大利润： $450（权利金全部到手）                                                                                                                  
  - 最大亏损： $24,550（如果被行权，以$250买入AAPL）                                                                                                   
  - 盈亏平衡点： $245.50（$250 - $4.50）                                                                                                               
  - 获利概率： 68.2%                                                                                                                                   
  - 所需资金： 约$25,000（现金担保）                                                                                                                   
                                                                                                                                                       
  为什么有效：                                                                                                                                         
                                                                                                                                                       
  1. $250低于200日均线$238.50，下方有强力支撑                                                                                                          
  2. 悲观目标价$235，即使跌到那里，你也是以$250买入AAPL — 但$250仍远低于当前$261
  3. 获利概率高达68.2%，意味着约2/3的情况你可以白赚$450权利金                                                                                          
  4. 即使被行权，你也是以$245.50的有效成本买入一只优质股票 — GBM称之为"回调时的优质复合股"                                                             
                                                                                                                                                       
  ---                                                                                                                                                  
  八、异常交易活动（聪明钱在做什么）                                                                                                                   
                                                                                                                                                       
  ┌───────┬──────┬────────┬────────┬────────┬────────┬─────────┬────────┬──────────┐
  │ 日期  │ 类型 │ 行权价 │ 到期日 │ 成交量 │ 未平仓 │ 量/仓比 │ 权利金 │   信号   │                                                                   
  ├───────┼──────┼────────┼────────┼────────┼────────┼─────────┼────────┼──────────┤                                                                   
  │ 04/09 │ 看涨 │ 280    │ 05/16  │ 42,000 │ 12,500 │ 3.36倍  │ $336万 │ 看多     │                                                                   
  ├───────┼──────┼────────┼────────┼────────┼────────┼─────────┼────────┼──────────┤                                                                   
  │ 04/08 │ 看跌 │ 245    │ 04/25  │ 32,000 │ 9,800  │ 3.27倍  │ $96万  │ 看跌对冲 │                                                                   
  └───────┴──────┴────────┴────────┴────────┴────────┴─────────┴────────┴──────────┘                                                                   
                                                                                                                                                       
  解读：                                                                                                                                               
                  
  这是典型的机构"买涨+对冲"策略：                                                                                                                      
                  
  - 主力方向： 大量买入5月到期$280看涨期权，押注财报后AAPL反弹至$280以上。成交量是未平仓量的3.36倍，说明是新开的仓位                                   
  - 同时对冲： 买入4月到期$245看跌期权做下行保护。如果财报暴雷跌破$245，看跌期权可以弥补损失
                                                                                                                                                       
  ---                                                                                                                                                  
  九、大盘情绪背景                                                                                                                                     
                                                                                                                                                       
  ┌────────────────┬────────────┬─────────────────────────┐
  │      指标      │    数值    │          含义           │                                                                                            
  ├────────────────┼────────────┼─────────────────────────┤                                                                                            
  │ VIX恐慌指数    │ 22.8       │ 62百分位 — 偏高但不极端 │                                                                                            
  ├────────────────┼────────────┼─────────────────────────┤                                                                                            
  │ 恐惧与贪婪指数 │ 38（恐惧） │ 市场整体谨慎            │                                                                                            
  ├────────────────┼────────────┼─────────────────────────┤                                                                                            
  │ SPY看跌/看涨比 │ 1.05       │ 市场略微防御性          │                                                                                            
  ├────────────────┼────────────┼─────────────────────────┤                                                                                            
  │ 板块轮动       │ 晚周期     │ 质量股受青睐            │
  └────────────────┴────────────┴─────────────────────────┘                                                                                            
                  
  对你的意义： 大盘处于"恐惧"状态，但AAPL作为质量股在晚周期中受到资金青睐。恐惧市场通常提供较好的期权卖方机会（IV偏高 → 权利金更贵）。                 
                  
  ---                                                                                                                                                  
  十、风险因素    
                                                                                                                                                       
  1. 22天后财报 — IV持续偏高，财报后暴跌约31%
  2. 贸易政策/关税风险 — 苹果供应链对中国依赖度高，关税政策影响大                                                                                      
  3. 低于50日均线 — $272.80形成上方阻力                                                                                                                
  4. 财报前IV高企 — 裸买看涨期权成本过高，强烈建议使用价差策略                                                                                         
                                                                                                                                                       
  ---                                                                                                                                                  
  总结：行动方案                                                                                                                                       
                                                                                                                                                       
  ┌──────────────┬──────────────────────────┬───────────────────────────────────────────┐
  │   你的观点   │         推荐交易         │                   理由                    │                                                              
  ├──────────────┼──────────────────────────┼───────────────────────────────────────────┤                                                              
  │ 看涨AAPL     │ 牛市看涨价差 265/280     │ 风险有限，减轻IV暴跌冲击，风险回报比2.6:1 │                                                              
  ├──────────────┼──────────────────────────┼───────────────────────────────────────────┤                                                              
  │ 赚取收入     │ 现金担保卖PUT $250       │ 68.2%胜率，$250是强支撑位                 │                                                              
  ├──────────────┼──────────────────────────┼───────────────────────────────────────────┤                                                              
  │ 对冲现有持仓 │ 买入4/25 $255看跌        │ 评分7.5，成本约$595/张，提供下行保护      │                                                              
  ├──────────────┼──────────────────────────┼───────────────────────────────────────────┤                                                              
  │ 赌财报方向   │ 避免裸买                 │ 历史31%的IV暴跌会吃掉大部分多头仓位       │
  ├──────────────┼──────────────────────────┼───────────────────────────────────────────┤                                                              
  │ 财报后交易   │ 等IV暴跌后再买入长期看涨 │ IV从~38%降到~27%，入场更便宜              │
  └──────────────┴──────────────────────────┴───────────────────────────────────────────┘                                                              
                  
  最佳交易： 现金担保看跌期权（CSP）在$250行权价 — 评分最高（8.0）、胜率最高（68.2%）、与GBM"回调买入优质股"的核心观点一致。                           
                  
  ---                                                                                                                                                  
  如果你对某个具体策略想深入了解，或者想让我模拟某个策略在不同股价路径下的盈亏情况，随时告诉我。
                                                                                                                                                       
✻ Baked for 1m 32s
                                                                                          
❯ exit 
                                                                                                                                                       
Resume this session with:
claude --resume f16fd32b-0b6e-48d7-88ac-85eca60a7f1b
(base) peilongchencc@chenpeilongdeMacBook-Pro AlphaGBMskills % 
