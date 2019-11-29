#-*-coding:utf-8-*- 
__author__ = 'AeenPython'

js1 = '''() =>{

           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }'''

js2 = '''() => {
        alert (
            window.navigator.webdriver
        )
    }'''

js3 = '''() => {
        window.navigator.chrome = {
    runtime: {},
    // etc.
  };
    }'''

js4 = '''() =>{
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
        }'''

js5 = '''() =>{
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
        }'''
js6 = '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }'''
js7 = '''() =>{ window.navigator.chrome = { runtime: {},  }; }'''
js8 = '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }'''
js9 = '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }'''
