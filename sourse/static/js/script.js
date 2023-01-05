let slideUp = (target, duration = 400) => {
   if (!target.classList.contains('-anim')) {
      target.classList.add('-anim');
      target.style.transitionProperty = 'height, margin, padding';
      target.style.transitionDuration = duration + 'ms';
      target.style.height = target.offsetHeight + 'px';
      target.offsetHeight;
      target.style.overflow = 'hidden';
      target.style.height = 0;
      target.style.paddingTop = 0;
      target.style.paddingBottom = 0;
      target.style.marginTop = 0;
      target.style.marginBottom = 0;
      window.setTimeout(() => {
         target.hidden = true;
         target.style.removeProperty('height');
         target.style.removeProperty('padding-top');
         target.style.removeProperty('padding-bottom');
         target.style.removeProperty('margin-top');
         target.style.removeProperty('margin-bottom');
         target.style.removeProperty('overflow');
         target.style.removeProperty('transition-duration');
         target.style.removeProperty('transition-property');
         target.classList.remove('-anim');
      }, duration)
   }
}
let slideDown = (target, duration = 400) => {
   if (!target.classList.contains('-anim')) {
      target.classList.add('-anim');
      if (target.hidden) {
         target.hidden = false;
      }
      let height = target.offsetHeight;
      target.style.overflow = 'hidden';
      target.style.height = 0;
      target.style.paddingTop = 0;
      target.style.paddingBottom = 0;
      target.style.marginTop = 0;
      target.style.marginBottom = 0;
      target.offsetHeight;
      target.style.transitionProperty = 'height, margin, padding';
      target.style.transitionDuration = duration + 'ms';
      target.style.height = height + 'px';
      target.style.removeProperty('padding-top');
      target.style.removeProperty('padding-bottom');
      target.style.removeProperty('margin-top');
      target.style.removeProperty('margin-bottom');
      window.setTimeout(() => {
         target.style.removeProperty('height');
         target.style.removeProperty('overflow');
         target.style.removeProperty('transition-duration');
         target.style.removeProperty('transition-property');
         target.classList.remove('-anim');
      }, duration)
   }
}
let slideToggle = (target, duration = 400) => {
   if (target.hidden) {
      return slideDown(target, duration);
   } else {
      return slideUp(target, duration);
   }
}
function testWebP(callback) {
   var webP = new Image();
   webP.onload = webP.onerror = function () {
      callback(webP.height == 2);
   };
   webP.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
}
testWebP(function (support) {
   if (support == true) {
      document.querySelector('body').classList.add('webp');
   }
});
class Me {
   constructor(type) {
      this.typeMedia = type
   }
   init() {
      this.elements = document.querySelectorAll('[data-me]')
      this.objects = []

      if (this.elements.length > 0) {
         for (let index = 0; index < this.elements.length; index++) {
            const meElement = this.elements[index];

            const obj = {}
            obj.el = meElement
            const dataAttr = meElement.dataset.me.split(',').map(item => item.trim())
            obj.dataAttr = {
               size: dataAttr[0],
               block: dataAttr[1],
               index: dataAttr[2],
            }
            obj.parentElement = obj.el.parentElement
            obj.indexParent = Array.from(obj.parentElement.children).indexOf(obj.el)
            this.objects.push(obj)
         }
         for (let index = 0; index < this.objects.length; index++) {
            const obj = this.objects[index];
            const mediaQueryList = window.matchMedia(`(${this.typeMedia}-width:${obj.dataAttr.size}px)`)
            this.mediaHandler(mediaQueryList, obj)
            mediaQueryList.addEventListener('change', e => this.mediaHandler(e, obj))
         }
      }
   }
   mediaHandler(e, obj) {
      if (e.matches) {
         obj.el.classList.add('-me')
         this.moveTo(obj.el, obj.dataAttr.block, obj.dataAttr.index)
      } else {
         obj.el.classList.remove('-me')
         this.moveBack(obj.el, obj.parentElement, obj.indexParent)
      }
   }
   moveTo(element, block, index) {
      if (document.querySelector(block)) {
         const toBlock = document.querySelector(block)
         const blockChildren = toBlock.children
         const indexBlock = index == 'first' ? 0 :
            index == 'last' ? undefined :
               index;

         if (blockChildren[indexBlock] != undefined) {
            blockChildren[indexBlock].insertAdjacentElement(
               'beforebegin',
               element
            )
         } else {
            toBlock.insertAdjacentElement(
               'beforeend',
               element
            )
         }
      }
   }
   moveBack(element, parentElement, index) {
      const blockChildren = parentElement.children

      if (blockChildren[index] != undefined) {
         blockChildren[index].insertAdjacentElement(
            'beforebegin',
            element
         )
      } else {
         parentElement.insertAdjacentElement(
            'beforeend',
            element
         )
      }
   }
}
const me = new Me('max')
me.init()
const regexPasswordValid = /(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{6,}/
// class ValidateForm {
//    constructor(form, objUser) {
//       this.form = form
//       this.objUser = objUser
//       form.addEventListener('submit', e => this.formSend(e, this, form, objUser))
//       if(form.classList.contains('-event-change')) {
//          form.addEventListener('change', e => this.formSend(e, this, form, objUser))
//       }
//    }
//    async formSend(e, thisClass, form, objUser) {
//       e.preventDefault()
//       const error = thisClass.validateForm(form, objUser)

//       if (error === 0) {
//          form.classList.add('-sending')
//          const formData = new FormData(form)

//          const response = await fetch(objUser.url, {
//             method: objUser.method,
//             // body: formData
//          })
//          if (response.ok) {
//             // const result = await response.json();
//             console.log('result');
//          } else {
//             console.log('Error');
//          }

//          if(!form.classList.contains('-event-change')) {
//             form.reset()
//             if (form.querySelectorAll('.-custom-select')) {
//                const customSelect = form.querySelectorAll('.-custom-select')
//                customSelect.forEach(select => select.reset())
//             }
//             if (objUser.items.input && objUser.items.input.length > 0) {
//                objUser.items.input.forEach(input => {
//                   input.blur()
//                })
//             }
//          }
//          form.classList.remove('-sending')
//       } else {
//          console.log('Emptly');
//       }
//    }
//    validateForm(form, objUser) {
//       let error = 0;
//       for (const prop in objUser.items) {
//          const elements = objUser.items[prop]

//          if (prop == 'input') {
//             if (elements.length > 0) {
//                elements.forEach(input => {
//                   this.removeError(input)

//                   if (input.classList.contains('-tel')) {
//                      if (this.telTest(input)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-tel-code')) {
//                      const selectCode = input.closest('.login-form__input').previousElementSibling.querySelector('select')
//                      const fullTel = (selectCode.value + input.value).replace('+', '')
//                      if (this.telCodeTest(fullTel)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-tel-code-input')) {
//                      const inputCode = input.parentElement.previousElementSibling.querySelector('input')
                     
//                      if(!/(?=.*[0-9])/.test(inputCode.value)) {
//                         this.addError(inputCode)
//                         error++
//                      }else {
//                         const fullPhone = inputCode.value+input.value
//                         if (this.telCodeTest(fullPhone)) {
//                            this.addError(input)
//                            error++
//                         }
//                      }
//                   } else if (input.classList.contains('-email')) {
//                      if (this.emailTest(input)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-email-phone')) {
//                      if (this.emailTest(input)) {
//                         if (this.telTest(input)) {
//                            this.addError(input)
//                            error++
//                         }
//                      }
//                   } else if (input.classList.contains('-date')) {
//                      if (this.dateTest(input)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-password-valid')) {
//                      if (this.passwordValidTest(input)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-password')) {
//                      if (this.passwordValidTest(input)) {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-file')) {
//                      if (input.value == '') {
//                         this.addError(input)
//                         error++
//                      }
//                   } else if (input.classList.contains('-number')) {
//                      const inputMinValue = +input.min
//                      const inputMaxValue = +input.max
//                      const inputValue = +input.value
//                      const valuesFilter = input.closest('.values-form-filter')
                     
//                      if(input.value!=='') {
//                         if(input.hasAttribute('min') && input.hasAttribute('max')) {
//                            if(inputValue < inputMinValue || inputValue> inputMaxValue) {
//                               this.addError(input)
//                               error++
//                            }
//                         }else {
//                            if(input.classList.contains('-number-min')) {
//                               if(inputValue < inputMinValue) {
//                                  this.addError(input)
//                                  error++
//                               }
//                            }
//                            if(input.classList.contains('-number-max')) {
//                               if(inputValue < inputMinValue) {
//                                  this.addError(input)
//                                  error++
//                               }
//                               const inputElMinValue = valuesFilter.querySelector('.-number-min')
//                               if(inputElMinValue.value!=='') {
//                                  if(inputValue < +inputElMinValue.value) {
//                                     this.addError(input)
//                                     error++
//                                  }
//                               }
//                            }
//                         }
//                      }
//                   }
//                   else {
//                      if (!input.value) {
//                         this.addError(input)
//                         error++
//                      }
//                   }
//                })
//             }
//          }
//          if (prop == 'checkbox') {
//             if (elements.length > 0) {
//                elements.forEach(checkbox => {
//                   this.removeError(checkbox)
//                   if (!checkbox.checked) {
//                      this.addError(checkbox)
//                      error++
//                   }
//                })
//             }
//          }
//          if (prop == 'radio') {
//             if (elements.length > 0) {
//                const groupsRadio = {}
//                elements.forEach(radio => {
//                   if (!groupsRadio[radio.name]) {
//                      groupsRadio[radio.name] = []
//                   }
//                   groupsRadio[radio.name].push(radio)
//                })
//                for (const prop in groupsRadio) {
//                   const groupRadio = groupsRadio[prop]
//                   const checkedRadio = Array.from(groupRadio).filter(radio => radio.checked)[0]

//                   groupRadio.forEach(radio => {
//                      this.removeError(radio)
//                   })
//                   if (!checkedRadio) {
//                      groupRadio.forEach(radio => {
//                         this.addError(radio)
//                         error++
//                      })
//                   }
//                }
//             }
//          }
//          if (prop == 'select') {
//             if (elements.length > 0) {
//                elements.forEach(select => {
//                   select.classList.remove('-error')
//                   if (select.classList.contains('-custom-select-no-choose')) {
//                      select.classList.add('-error')
//                      error++
//                   }
//                })
//             }
//          }
//       }
//       return error;
//    }
//    removeError(input) {
//       input.parentElement.classList.remove('-error')
//       input.classList.remove('-error')
//       const form = input.closest('form')
//       if (form.classList.contains('-error')) {
//          form.classList.remove('-error')
//       }
//    }
//    addError(input) {
//       input.parentElement.classList.add('-error')
//       input.classList.add('-error')
//       const form = input.closest('form')
//       if (!form.classList.contains('-error')) {
//          form.classList.add('-error')
//       }
//    }
//    emailTest(input) {
//       return !/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,8})+$/.test(input.value);
//    }
//    telTest(input) {
//       return !/^((8|\+7)[\- ]?)?(\(?\d{3,4}\)?[\- ]?)?[\d\- ]{5,10}$/.test(input.value);
//    }
//    telCodeTest(value) {
//       return !/^((8|\+7)[\- ]?)?(\(?\d{3,4}\)?[\- ]?)?[\d\- ]{5,10}$/.test(value);
//    }
//    passwordValidTest(input) {
//       return !regexPasswordValid.test(input.value)
//    }
//    dateTest(input) {
//       if(input.value == '') {
//          return true;
//       }else {
//          return false;
//       }
//    }
// }

const inputsValue = document.querySelectorAll('[data-value]')
if (inputsValue.length > 0) {
   inputsValue.forEach(input => {
      const placeholderValue = input.dataset.value;

      if (!input.value) {
         input.placeholder = placeholderValue
      }

      input.addEventListener('focus', () => {
         input.placeholder = ''
      })
      input.addEventListener('blur', () => {
         input.placeholder = placeholderValue
      })
   })
}
class Tabs {
   init() {
      this.elements = document.querySelectorAll('[data-tab]')
      this.objects = []
      if (this.elements.length > 0) {
         for (let index = 0; index < this.elements.length; index++) {
            const tab = this.elements[index];
            const obj = {}
            obj.el = tab
            obj.itemLabel = obj.el.hasAttribute('data-tab-item-label')
            if (obj.el.children[0].children[0]) {
               if (obj.el.children[0].children[0].hasAttribute('data-tab-item')) {
                  obj.items = Array.from(obj.el.children[0].children)
               } else if (obj.el.children[0].children[0].hasAttribute('data-tab-subitem')) {
                  obj.items = Array.from(obj.el.children[0].children)
               } else if (obj.el.children[0].children[0].hasAttribute('data-tab-item')) {
                  obj.items = Array.from(obj.el.children[0].children)
               }else {
                  obj.items = Array.from(obj.el.querySelectorAll('[data-tab-item]'))
               }
            }
            
            if(obj.itemLabel) {
               obj.items = Array.from(obj.el.querySelectorAll('[data-tab-subitem]'))
            }

            obj.contents = Array.from(obj.el.children[1].children)
            obj.activeItems = Array.from(obj.items).filter(item => item.classList.contains('-active'))

            const mediaSettings = obj.el.dataset.tab.split(',').map(item => item.trim())
            obj.mediaSettings = {
               type: mediaSettings[0],
               size: mediaSettings[1],
            }
            this.objects.push(obj)
         }
         for (let index = 0; index < this.objects.length; index++) {
            const obj = this.objects[index];
            const mediaQueryList = window.matchMedia(`(${obj.mediaSettings.type}-width:${obj.mediaSettings.size}px)`)
            this.mediaHandler(mediaQueryList, obj.el, obj.items, obj.contents, obj.activeItems, obj.itemLabel, obj)
            mediaQueryList.addEventListener('change', e => this.mediaHandler(e, obj.el, obj.items, obj.contents, obj.activeItems, obj.itemLabel, obj))
         }
      }
   }
   mediaHandler(e, tabElement, items, contents, activeItems, itemLabel, obj) {
      if (e.matches) {
         let activeItems = []
         const inactiveItems = []
         items.forEach(item => item.classList.contains('-active') ? activeItems.push(item) : inactiveItems.push(item))
         if (activeItems.length > 0) {
            if (activeItems.length > 1) {
               items.forEach(item => item.classList.remove('-active'))
               items[0].classList.add('-active')
               activeItems = [items[0]]
               if (itemLabel) {
                  slideDown(activeItems[0].nextElementSibling, 0)
               }
            }
            if (itemLabel) {
               activeItems.forEach(item => slideDown(item.nextElementSibling, 0))
               items.forEach(item => {
                  if (item.hasAttribute('data-spoller-item-next')) {
                     slideUp(item.nextElementSibling.nextElementSibling, 0)
                  } else {
                     slideUp(item.nextElementSibling, 0)
                  }
               })
            }
         } else {
            items[0].classList.add('-active')
            activeItems = [items[0]]
            if (itemLabel) {
               activeItems.forEach(item => slideDown(item.nextElementSibling, 0))
               items.forEach(item => {
                  if (item.hasAttribute('data-spoller-item-next')) {
                     slideUp(item.nextElementSibling.nextElementSibling, 0)
                  } else {
                     slideUp(item.nextElementSibling, 0)
                  }
               })
            }
         }
         const activeContent = []
         const inactiveContent = []
         if (activeItems[0].dataset.tabItem) {
            contents.forEach(content => content.dataset.tabContent == activeItems[0].dataset.tabItem ? activeContent.push(content) : inactiveContent.push(content))
         } else if (activeItems[0].dataset.tabSubitem) {
            contents.forEach(content => content.dataset.tabContent == activeItems[0].dataset.tabSubitem ? activeContent.push(content) : inactiveContent.push(content))
         }

         activeContent[0].classList.add('-active')
         this.animShow(activeContent[0], false)

         inactiveContent.forEach(content => {
            if (content.classList.contains('-active')) {
               content.classList.remove('-active')
            }
            this.animHide(content, false)
         })

         tabElement.contents = contents
         tabElement.thisCLass = this
         tabElement.items = items
         tabElement.itemLabel = itemLabel
         tabElement.addEventListener('click', this.actionTabElement)
      } else {
         items.forEach(item => {
            item.classList.remove('-active')
            if (itemLabel) {
               items.forEach(item => {
                  slideDown(item.nextElementSibling, 0)
               })
            }
         })
         contents.forEach(content => {
            content.classList.remove('-active')
            this.animShow(content, false, true)
         })
         if (activeItems) {
            activeItems.forEach(item => item.classList.add('-active'))
         }

         tabElement.removeEventListener('click', this.actionTabElement)
      }
   }
   actionTabElement(e) {
      const target = e.target
      const contents = e.currentTarget.contents
      const thisCLass = e.currentTarget.thisCLass
      const itemLabel = e.currentTarget.itemLabel
      
      if (target.closest('[data-tab-item]') || target.closest('[data-tab-subitem]') && target.closest('.-parent-tab-item')) {
         e.preventDefault()
         let animContents;
         let contentsElement;

         let items;
         if(itemLabel) {
            items = target.closest('.-parent-tab-item').querySelectorAll('[data-tab-subitem]')
         }else {
            items = target.closest('.-parent-tab-item').children

         }
         if (target.closest('[data-tab-item]')) {
            if(target.closest('[data-tab-item]').closest('[data-tab-items]').nextElementSibling){
               contentsElement = target.closest('[data-tab-item]').closest('[data-tab-items]').nextElementSibling.children
            }else {
               contentsElement = target.closest('[data-tab-item]').closest('[data-tab]').children[1].children
            }
         } else if (target.closest('[data-tab-subitem]')) {
            contentsElement = target.closest('[data-tab-subitem]').closest('[data-tab-items]').nextElementSibling.children
         }

         animContents = Array.from(contentsElement).filter(content => content.classList.contains('-anim'))
         if (animContents.length === 0) {
            let item;
            if (target.closest('[data-tab-item]')) {
               item = target.closest('[data-tab-item]')
            } else if (target.closest('[data-tab-subitem]')) {
               item = target.closest('[data-tab-subitem]')
            }

            if (!item.classList.contains('-active')) {
               let activeContent = [];
               const inactiveContent = []
               if (item.dataset.tabItem) {
                  contents.forEach(content => content.dataset.tabContent == item.dataset.tabItem ? activeContent.push(content) : inactiveContent.push(content))
               } else if (item.dataset.tabSubitem) {
                  contents.forEach(content => content.dataset.tabContent == item.dataset.tabSubitem ? activeContent.push(content) : inactiveContent.push(content))
               }
               Array.from(items).forEach(item => item.classList.remove('-active'))
               item.classList.add('-active')

               activeContent[0].classList.add('-active')

               thisCLass.animShow(activeContent[0])
               inactiveContent.forEach(content => {
                  thisCLass.animHide(content)
                  content.classList.remove('-active')
               })
               setTimeout(() => {
                  ssb.refresh()
               }, 150)
               if (itemLabel) {
                  slideDown(item.nextElementSibling)
                  Array.from(items).forEach(item => {
                     slideUp(item.nextElementSibling)
                  })
               }
            }
         }
      }
   }
   animHide(el, anim = true) {
      if (anim) {
         el.style.opacity = '0.5'
         el.classList.add('-anim')
         setTimeout(() => {
            el.style.display = 'none'
            el.classList.remove('-anim')
         }, 150)
      } else {
         el.style.opacity = '0.5'
         el.style.display = 'none'
      }
   }
   animShow(el, anim = true, removeStyle = false) {
      if (anim) {
         setTimeout(() => {
            el.style.display = 'block'
            el.classList.add('-anim')
            setTimeout(() => {
               el.style.opacity = '1'
               el.classList.remove('-anim')
            }, 100)
         }, 150)
      } else {
         el.style.opacity = '1'
         el.style.display = 'block'
      }
      if (removeStyle) {
         el.style.removeProperty('opacity')
         el.style.removeProperty('display')
      }
   }
}
const tabs = new Tabs()
tabs.init()
class CustomSelect {
   init() {
      this.elements = document.querySelectorAll('[data-custom-select]')
      this.objects = []
      if (this.elements.length > 0) {
         for (let index = 0; index < this.elements.length; index++) {
            const select = this.elements[index];

            const obj = {}
            obj.select = select
            obj.options = obj.select.options
            obj.selectedIndex = obj.select.selectedIndex
            obj.className = obj.select.classList[0]
            obj.mLabel = obj.select.hasAttribute('data-custom-select-mlabel') ? obj.select.dataset.customSelectMlabel : false
            obj.label = obj.select.hasAttribute('data-custom-select-label') ? obj.select.dataset.customSelectLabel : false

            this.objects.push(obj)
         }
         for (let index = 0; index < this.objects.length; index++) {
            const obj = this.objects[index];
            obj.select.className = ''
            obj.select.style.display = 'none'
            this.createStructure(obj.select, obj.options, obj.className, obj.mLabel, obj.label)

            obj.customSelect = {}
            obj.customSelect.select = obj.select.nextElementSibling
            obj.customSelect.openner = obj.customSelect.select.querySelector('.-custom-select__openner')
            obj.customSelect.value = obj.customSelect.select.querySelector('.-custom-select__value')
            obj.customSelect.icon = obj.customSelect.select.querySelector('.-custom-select__icon')
            obj.customSelect.body = obj.customSelect.select.querySelector('.-custom-select__body')
            obj.customSelect.items = obj.customSelect.select.querySelectorAll('.-custom-select__item')
            this.fillContent(obj)

            const customSelect = obj.customSelect

            if (!obj.label) {
               customSelect.items[obj.select.selectedIndex].classList.add('-active')
            } else {
               customSelect.select.classList.add('-custom-select-no-choose')
            }

            slideUp(customSelect.body, 0)
            customSelect.select.addEventListener('click', e => this.actionCustomSelect(e, obj.label, obj.select, obj.options))
            document.addEventListener('click', this.actionDocument)

            const thisClass = this
            customSelect.select.reset = function () {
               const activeItem = customSelect.items[obj.selectedIndex]
               thisClass.activeOption(activeItem, obj.select, obj.options, customSelect.select, obj.label)
            }
         }
      }
   }
   createStructure(select, options, className, mLabel, label) {
      const templateWrapStart = `<div class="${className} -custom-select">`
      const templateWrapEnd = `</div>`

      const templateOpennerStart = `<a href="" class="${className}__openner -custom-select__openner">`
      const templateOpennerEnd = `</a>`
      const templateValue = `<div class="${className}__value -custom-select__value">${label ? label : ''}</div>`
      const templateIcon = `<div class="${className}__icon -custom-select__icon"></div>`

      const templateMlable = mLabel ? `<div class="${className}__mlabel -custom-select__mlabel">${mLabel}</div>` : ''
      const templateOpenner = templateOpennerStart + templateMlable + templateValue + templateIcon + templateOpennerEnd

      const templateBodyStart = `<div class="${className}__body -custom-select__body">`
      const templateBodyEnd = `</div>`
      let templateItems = ''
      for (let index = 0; index < options.length; index++) {
         const templateItem = `<div class="${className}__item -custom-select__item"></div>`
         templateItems += templateItem
      }
      const templateBody = templateBodyStart + templateItems + templateBodyEnd
      const templateCustomSelect = templateWrapStart + templateOpenner + templateBody + templateWrapEnd
      select.insertAdjacentHTML(
         'afterend',
         templateCustomSelect
      )
   }
   fillContent(obj) {
      const selectedOption = obj.options[obj.select.selectedIndex]
      if (!obj.label) {
         obj.customSelect.value.innerHTML = selectedOption.innerHTML
      }

      const contentOptions = Array.from(obj.options).map(item => item.innerHTML)
      obj.customSelect.items.forEach((item, index) => item.innerHTML = contentOptions[index])
   }
   actionCustomSelect(e, label, select, options) {
      const target = e.target
      const customSelect = e.currentTarget
      const customSelectValue = customSelect.querySelector('.-custom-select__value')
      const customSelectBody = customSelect.querySelector('.-custom-select__body')
      const customSelectItems = customSelect.querySelectorAll('.-custom-select__item')

      if (target.closest('.-custom-select__item')) {
         if (!document.querySelector('.-custom-select__body.-anim')) {
            if (label && customSelect.classList.contains('-custom-select-no-choose')) {
               customSelect.classList.remove('-custom-select-no-choose')
            }
            if (!target.classList.contains('-active')) {
               this.activeOption(target, select, options, customSelect)
            }
            customSelect.classList.remove('-open')
            slideUp(customSelectBody)
         }
      }
      if (target.closest('.-custom-select__openner')) {
         e.preventDefault()

         if (!document.querySelector('.-custom-select__body.-anim')) {
            const openner = target.closest('.-custom-select__openner')
            if (document.querySelector('.-custom-select.-open')) {
               const openCustomSelect = document.querySelector('.-custom-select.-open')

               if (openCustomSelect != customSelect) {
                  const customSelectBody = openCustomSelect.querySelector('.-custom-select__body')
                  slideUp(customSelectBody)
                  openCustomSelect.classList.remove('-open')
               }
            }

            if (!customSelect.classList.contains('-open')) {
               openner.vars = [this, select, options, customSelect, customSelectValue, customSelectBody, customSelectItems, label]
               openner.addEventListener('keydown', this.keydownOpenner)
               document.addEventListener('keydown', this.keydownDocument)
               openner.addEventListener('blur', this.blurOpenner)
            } else {
               openner.vars = []
               openner.removeEventListener('blur', this.blurOpenner)
               openner.removeEventListener('keydown', this.keydownOpenner)
               document.removeEventListener('keydown', this.keydownDocument)
            }

            customSelect.classList.toggle('-open')
            slideToggle(customSelectBody)
         }
      }
   }
   blurOpenner(e) {
      if (!document.querySelector('.-custom-select__body.-anim')) {
         const openner = e.target
         const thisClass = openner.vars[0]
         const customSelect = openner.vars[3]
         const customSelectBody = openner.vars[5]
         if (openner.eventKey == 'Tab') {
            customSelect.classList.remove('-open')
            slideUp(customSelectBody)
            openner.eventKey = undefined
         }

         openner.removeEventListener('blur', thisClass.blurOpenner)
         openner.removeEventListener('keydown', thisClass.keydownOpenner)
         document.removeEventListener('keydown', thisClass.keydownDocument)
      }

   }
   keydownDocument(e) {
      if (e.code == 'ArrowUp' || e.code == 'ArrowDown') {
         e.preventDefault()
      }
   }
   keydownOpenner(e) {
      const openner = e.target
      const thisClass = openner.vars[0]
      const select = openner.vars[1]
      const options = openner.vars[2]
      const customSelect = openner.vars[3]
      const customSelectValue = customSelect.querySelector('.-custom-select__value')
      const customSelectBody = customSelect.querySelector('.-custom-select__body')
      const customSelectItems = customSelect.querySelectorAll('.-custom-select__item')
      const label = openner.vars[7]

      openner.eventKey = e.code

      if (e.code == 'Tab' && document.querySelector('.-custom-select__body.-anim')) {
         e.preventDefault()
      }

      if (!document.querySelector('.-custom-select__body.-anim')) {
         if (e.code == 'Escape') {
            customSelect.classList.remove('-open')
            slideUp(customSelectBody)
         }
         if (e.code == 'ArrowUp' || e.code == 'ArrowDown') {
            let activeItem = customSelect.querySelector('.-custom-select__item.-active')

            if (!activeItem) {
               activeItem = customSelectItems[0]
               thisClass.activeOption(activeItem, select, options, customSelect)

               if (label && customSelect.classList.contains('-custom-select-no-choose')) {
                  customSelect.classList.remove('-custom-select-no-choose')
               }

               return false;
            }
            if (e.code == 'ArrowUp' && activeItem.previousElementSibling) {
               thisClass.activeOption(activeItem.previousElementSibling, select, options, customSelect)
            }
            if (e.code == 'ArrowDown' && activeItem.nextElementSibling) {
               thisClass.activeOption(activeItem.nextElementSibling, select, options, customSelect)
            }
         }
      }
   }
   activeOption(item, select, options, customSelect, label = null) {
      const customSelectValue = customSelect.querySelector('.-custom-select__value')
      const customSelectItems = customSelect.querySelectorAll('.-custom-select__item')

      customSelectItems.forEach(item => item.classList.remove('-active'))
      select.selectedIndex = Array.from(customSelectItems).indexOf(item)
      if (!label) {
         const selectedIndex = select.selectedIndex
         customSelectItems[selectedIndex].classList.add('-active')

         customSelectValue.innerHTML = options[selectedIndex].innerHTML
      } else {
         customSelectValue.innerHTML = label
         const customSelect = customSelectValue.closest('.-custom-select')
         customSelect.classList.add('-custom-select-no-choose')
      }
   }
   actionDocument(e) {
      const target = e.target
      if (!target.closest('.-custom-select')) {
         if (document.querySelector('.-custom-select.-open')) {
            if (!document.querySelector('.-custom-select__body.-anim')) {
               const activeCustomSelect = document.querySelector('.-custom-select.-open')
               const customSelectBody = activeCustomSelect.querySelector('.-custom-select__body')

               activeCustomSelect.classList.remove('-open')
               slideUp(customSelectBody)
            }
         }
      }
   }
}
const customSelect = new CustomSelect()
customSelect.init()
class Spoller {
   init() {
      this.elements = document.querySelectorAll('[data-spollers]')
      this.objects = []
      if (this.elements.length > 0) {
         for (let index = 0; index < this.elements.length; index++) {
            const spoller = this.elements[index];
            const obj = {}
            obj.el = spoller
            obj.oneSpoller = obj.el.hasAttribute('data-one-spoller')
            obj.items = obj.el.querySelectorAll('[data-spoller-item]')
            const mediaSettings = obj.el.dataset.spollers.split(',').map(item => item.trim())
            obj.mediaSettings = {
               type: mediaSettings[0],
               size: mediaSettings[1],
            }
            obj.activeItems = Array.from(obj.items).filter(item => item.classList.contains('-active'))
            this.objects.push(obj)
         }
         for (let index = 0; index < this.objects.length; index++) {
            const obj = this.objects[index];
            const mediaQueryList = window.matchMedia(`(${obj.mediaSettings.type}-width:${obj.mediaSettings.size}px)`)

            this.mediaHandler(mediaQueryList, obj.el, obj.items, obj.activeItems, obj.oneSpoller)
            mediaQueryList.addEventListener('change', e => this.mediaHandler(e, obj.el, obj.items, obj.activeItems, obj.oneSpoller))
         }
      }
   }
   mediaHandler(e, spollerElement, items, activeItems, oneSpoller) {
      if (e.matches) {
         if(spollerElement.classList.contains('filter__body')) {
            document.body.classList.remove('-lock')
            document.querySelector('.filter__form').classList.remove('-open')
         }
         const activeItems = []
         const inactiveItems = []
         items.forEach(item => item.classList.contains('-active') ? activeItems.push(item) : inactiveItems.push(item))

         if (activeItems.length > 0) {
            if (oneSpoller) {
               if (activeItems.length > 1) {
                  slideDown(items[0].nextElementSibling, 0)
                  activeItems.forEach(item => {
                     item.classList.remove('-active')
                     slideUp(item.nextElementSibling, 0)
                  })
                  items[0].classList.add('-active')
               } else if (activeItems.length == 1) {
                  slideDown(activeItems[0].nextElementSibling, 0)
               }
            } else {
               activeItems.forEach(item => {
                  slideDown(item.nextElementSibling, 0)
               })
            }
         } else {
            if (oneSpoller) {
               items[0].classList.add('-active')
               slideDown(items[0].nextElementSibling, 0)
            }
         }
         if (inactiveItems.length > 0) {
            inactiveItems.forEach(item => {
               slideUp(item.nextElementSibling, 0)
            })
         }
         
         spollerElement.items = items
         spollerElement.oneSpoller = oneSpoller
         spollerElement.addEventListener('click', this.actionSpollerElement)
      } else {
         if(spollerElement.querySelector('[data-spollers]')){
            document.querySelectorAll('[data-spoller-item-1]').forEach(item => {
               item.classList.remove('-active')
               slideDown(item.nextElementSibling, 0)
            })
            document.querySelectorAll('[data-spoller-item-2]').forEach(item => {
               item.classList.remove('-active')
               slideDown(item.nextElementSibling, 0)
            })
         }else {
            items.forEach(item => {
               item.classList.remove('-active')
               slideDown(item.nextElementSibling, 0)
            })
         }
         if (activeItems.length > 0) {
            activeItems.forEach(item => item.classList.add('-active'))
         }
         
         if(spollerElement.items && spollerElement.oneSpoller) {
            delete spollerElement.items
            delete spollerElement.oneSpoller
         }
         spollerElement.removeEventListener('click', this.actionSpollerElement)
      }
   }
   actionSpollerElement(e) {
      const target = e.target;
      const items = e.currentTarget.items;
      const oneSpoller = e.currentTarget.oneSpoller;
      const animContent = Array.from(items).filter(item => item.nextElementSibling.classList.contains('-anim'))

      if (target.closest('[data-spoller-item]')) {
         const item = target.closest('[data-spoller-item]')
         if (!item.querySelector('[data-spoller-openner]') || target.closest('[data-spoller-openner]')) {
            e.preventDefault()
            if (animContent.length === 0) {
               if (item.classList.contains('-active')) {
                  if (!oneSpoller) {
                     item.classList.remove('-active')
                     slideUp(item.nextElementSibling)
                  }
               } else {
                  slideDown(item.nextElementSibling)
                  if (oneSpoller) {
                     items.forEach(item => {
                        item.classList.remove('-active')
                        slideUp(item.nextElementSibling)
                     })
                  }
                  item.classList.add('-active')
               }
            }
         }
      }
   }
}
const spoller = new Spoller()
spoller.init()
class CsSelect {
   init() {
      this.elements = document.querySelectorAll('[data-select]')
      this.objects = []
      if (this.elements.length > 0) {
         for (let index = 0; index < this.elements.length; index++) {
            const select = this.elements[index];

            const obj = {}
            obj.select = select
            obj.options = obj.select.options
            obj.selectedIndex = obj.select.selectedIndex
            obj.className = obj.select.classList[0]

            this.objects.push(obj)
         }
         for (let index = 0; index < this.objects.length; index++) {
            const obj = this.objects[index];

            obj.customSelect = {}
            obj.customSelect.select = obj.select
            obj.customSelect.openner = obj.select.querySelector('.-select__openner')
            obj.customSelect.value = obj.select.querySelector('.-select__value')
            obj.customSelect.icon = obj.select.querySelector('.-select__icon')
            obj.customSelect.body = obj.select.querySelector('.-select__body')
            obj.customSelect.items = obj.select.querySelectorAll('.-select__item')
            this.fillContent(obj)

            const customSelect = obj.customSelect

            slideUp(customSelect.body, 0)
            obj.select.addEventListener('click', e => this.actionCustomSelect(e, obj.select, obj.options))
            document.addEventListener('click', e=>this.actionDocument(e))
         }
      }
   }
   fillContent(obj) {
      obj.customSelect.value.innerHTML = obj.customSelect.body.querySelector('.-select__item.-active').innerHTML
   }
   actionCustomSelect(e, select, options) {
      const _this = this
      function start() {
         const target = e.target
         const customSelect = e.currentTarget
         const customSelectValue = customSelect.querySelector('.-select__value')
         const customSelectBody = customSelect.querySelector('.-select__body')
         const customSelectItems = customSelect.querySelectorAll('.-select__item')

         if (target.closest('.-select__item')) {
            if (!document.querySelector('.-select__body.-anim')) {
               const item = target.closest('.-select__item')
               if (!item.classList.contains('-active')) {
                  _this.activeOption(item, select)
               }
               customSelect.classList.remove('-open')
               slideUp(customSelectBody)
            }
         }
         if (target.closest('.-select__openner')) {
            e.preventDefault()
            if (!document.querySelector('.-select__body.-anim')) {
               const openner = target.closest('.-select__openner')
               if (document.querySelector('.-select.-open')) {
                  const openCustomSelect = document.querySelector('.-select.-open')

                  if (openCustomSelect != customSelect) {
                     const customSelectBody = openCustomSelect.querySelector('.-select__body')
                     slideUp(customSelectBody)
                     openCustomSelect.classList.remove('-open')
                  }
               }
               customSelect.classList.toggle('-open')
               slideToggle(customSelectBody)
            }
         }
      }
      start()
   }
   activeOption(item, customSelect) {
      const customSelectValue = customSelect.querySelector('.-select__value')
      item.parentElement.querySelectorAll('.-select__item').forEach(item=>item.classList.remove('-active'))
      item.classList.add('-active')
      customSelectValue.innerHTML = item.innerHTML
   }
   actionDocument(e) {
      function start(params) {
         const target = e.target
         if (!target.closest('.-select')) {
            if (document.querySelector('.-select.-open')) {
               if (!document.querySelector('.-select__body.-anim')) {
                  const activeCustomSelect = document.querySelector('.-select.-open')
                  const customSelectBody = activeCustomSelect.querySelector('.-select__body')
   
                  activeCustomSelect.classList.remove('-open')
                  slideUp(customSelectBody)
               }
            }
         }
      }
      start()
   }
}
const csSelect = new CsSelect()
csSelect.init()
let ssb = {
   aConts: [],
   mouseY: 0,
   N: 0,
   asd: 0, /*active scrollbar element*/
   sc: 0,
   sp: 0,
   to: 0,

   // constructor
   scrollbar: function (el) {
      // perform initialization
      if (!ssb.init()) return false;

      // adding new container into array
      ssb.aConts[ssb.N++] = el;

      el.insertAdjacentHTML(
         'afterbegin',
         '<div data-scroll-wrap></div>'
      )
      const customScrollWrap = el.querySelector('[data-scroll-wrap]')
      const customScrollContent = el.querySelector('[data-scroll-content]')
      customScrollWrap.insertAdjacentElement(
         'afterbegin',
         customScrollContent
      )
      customScrollWrap.insertAdjacentHTML(
         'afterend',
         `<div data-scroll-scrollbar>
            <div data-scroll-scrollbar-overlay></div>
            <div data-scroll-scrollbar-scroller></div>
         </div>`
      )
      customScrollWrap.wrap = el.querySelector('[data-scroll-scrollbar]')
      customScrollWrap.st = el.querySelector('[data-scroll-scrollbar-overlay]')
      customScrollWrap.sb = el.querySelector('[data-scroll-scrollbar-scroller]')
      // customScrollWrap.su = el.querySelector('[data-scroll-scrollbar-arrow-up]')
      // customScrollWrap.sd = el.querySelector('[data-scroll-scrollbar-arrow-down]')
      customScrollWrap.contentElement = customScrollContent

      if (isMobile.any()) {
         customScrollWrap.wrap.style.display = 'none'
         customScrollWrap.style.width = '100%'
         customScrollWrap.removeAttribute('data-scroll-hidden')
      } else {
         customScrollWrap.wrap.style.display = ''
         customScrollWrap.setAttribute('data-scroll-hidden', '')
      }

      el = customScrollWrap
      el.sw = customScrollWrap.wrap.offsetWidth
      el.sg = false;

      el.style.paddingRight = `${el.sw}px`

      // on mouse down processing
      el.sb.onmousedown = function (e) {
         if (!el.sg) {
            if (!e) e = window.event;

            ssb.asd = el;
            el.yZ = e.screenY;
            el.sZ = el.scrollTop;
            el.sg = true;
         }
         return false;
      }
      // on mouse down on free track area - move our scroll element too
      el.st.onmousedown = function (e) {
         if (!e) e = window.event;
         ssb.asd = el;
         let y
         
         if(ssb.asd.closest('[data-popup]')) {
            const elPopup = ssb.asd.closest('[data-popup]')
            ssb.mouseY = e.clientY + elPopup.scrollTop
            y = elPopup.scrollTop + ssb.asd.getBoundingClientRect().top
         }else {
            ssb.mouseY = e.clientY + window.scrollY;
            y = window.scrollY + ssb.asd.getBoundingClientRect().top
         }

         el.scrollTop = (ssb.mouseY - y - (el.ratio * el.offsetHeight / 2) - el.sw) / el.ratio;
         el.sb.onmousedown(e);
      }

      // onmousedown events
      // el.su.onmousedown = el.su.ondblclick = function (e) { ssb.mousedown(el, -1); return false; }
      // el.sd.onmousedown = el.sd.ondblclick = function (e) { ssb.mousedown(el, 1); return false; }

      //onmouseout events
      // el.su.onmouseout = el.su.onmouseup = ssb.clear;
      // el.sd.onmouseout = el.sd.onmouseup = ssb.clear;
      // onscroll - change positions of scroll element
      el.ssb_onscroll = function () {
         this.ratio = (this.offsetHeight) / this.scrollHeight;
         this.sb.style.top = `${Math.floor(this.scrollTop * this.ratio)}px`
      }

      // start scrolling
      el.ssb_onscroll();
      ssb.refresh();

      // binding own onscroll event
      el.onscroll = el.ssb_onscroll;
      return el;
   },

   // initialization
   init: function () {
      if (window.oper || (!window.addEventListener && !window.attachEvent)) { return false; }

      // temp inner function for event registration
      function addEvent(o, e, f) {
         if (window.addEventListener) { o.addEventListener(e, f, false); ssb.w3c = true; return true; }
         if (window.attachEvent) return o.attachEvent('on' + e, f);
         return false;
      }

      // binding events
      addEvent(window.document, 'mousemove', ssb.onmousemove);
      addEvent(window.document, 'mouseup', ssb.onmouseup);
      addEvent(window, 'resize', ssb.refresh);
      return true;
   },

   // create and append div finc
   create_div: function (c, el, cont_clone) {
      let o = document.createElement('div');
      o.el = el;
      o.className = c;
      cont_clone.appendChild(o);
      return o;
   },
   // // do clear of controls
   clear: function () {
      clearTimeout(ssb.to);
      ssb.sc = 0;
      return false;
   },
   // refresh scrollbar
   refresh: function () {
      for (let i = 0, N = ssb.N; i < N; i++) {
         let o = ssb.aConts[i].querySelector('[data-scroll-wrap]');
         o.ssb_onscroll();
         o.sb.style.height = `${Math.ceil(Math.max(o.sw * .5, o.ratio * o.offsetHeight))}px`

         if (o.contentElement.offsetHeight < o.offsetHeight) {
            o.wrap.style.display = 'none'
            o.style.paddingRight = '0px'
         }
      }
   },
   // // arrow scrolling
   // arrow_scroll: function () {
   //    if (ssb.sc != 0) {
   //       ssb.asd.scrollTop += 6 * ssb.sc / ssb.asd.ratio;
   //       ssb.to = setTimeout(ssb.arrow_scroll, ssb.sp);
   //       ssb.sp = 32;
   //    }
   // },

   /* event binded functions : */
   // scroll on mouse down
   mousedown: function (el, s) {
      if (ssb.sc == 0) {
         ssb.asd = el;
         ssb.sc = s;
         ssb.sp = 400;
         // ssb.arrow_scroll();
      }
   },
   // on mouseMove binded event
   onmousemove: function (e) {
      if (!e) e = window.event;
      // get vertical mouse position
      ssb.mouseY = e.screenY;

      if (ssb.asd.sg) ssb.asd.scrollTop = ssb.asd.sZ + (ssb.mouseY - ssb.asd.yZ) / ssb.asd.ratio;
   },
   // // on mouseUp binded event
   onmouseup: function (e) {
      if (!e) e = window.event;
      let tg = (e.target) ? e.target : e.srcElement;
      if (ssb.asd && document.releaseCapture) ssb.asd.releaseCapture();

      document.onselectstart = '';
      ssb.clear();
      ssb.asd.sg = false;
   }
}

window.onload = function () {
   const customScrollEl = document.querySelectorAll('[data-scroll]')
   if (customScrollEl.length) {
      customScrollEl.forEach(el => {
         ssb.scrollbar(el);
      })
   }
}
class Popup {
   init() {
      this.elements = document.querySelectorAll('[data-popup-link]')
      this.objects = []
      if (this.elements.length > 0) {
         document.addEventListener('click', e => this.actionPopupDocument(e, this))
      }
   }
   actionPopupDocument(e, thisClass) {
      const target = e.target
      const animPopup = document.querySelectorAll('[data-popup].-anim')

      if (target.closest('[data-popup-link]')) {
         e.preventDefault()

         if (animPopup.length === 0) {
            const popupLink = target.closest('[data-popup-link]')

            const openPopups = document.querySelectorAll('[data-popup].-open')
            openPopups.forEach(element => element.classList.remove('-open'))

            if (document.querySelector(`${popupLink.dataset.popupLink}`)) {
               const popupBlock = document.querySelector(`${popupLink.dataset.popupLink}`)
               if (openPopups.length > 0) {
                  thisClass.openPopup(popupBlock, false)
               } else {
                  thisClass.openPopup(popupBlock)
               }
            }
         }
      }
      if (target.closest('[data-popup-close]')) {
         e.preventDefault()
         if (animPopup.length === 0) {
            const popupClose = target.closest('[data-popup-close]')
            const popupBlock = popupClose.closest('[data-popup]')
            if(popupBlock.classList.contains('submit-popup-categories')) {
               const activeItems = popupBlock.querySelectorAll('.-categories-li.-active')
               if (activeItems.length > 0) {
                  activeItems.forEach(activeItem => {
                     const activeCol = activeItem.querySelector('.-categories-col.-open')
                     activeCol.classList.remove('-open')
                     activeItem.classList.remove('-active')
                  })
               }
            }
            thisClass.closePopup(popupBlock)
         }
      }
      if (target.closest('[data-popup]') && !target.closest('[data-popup-content]')) {
         if (animPopup.length === 0) {
            const popupBlock = target.closest('[data-popup]')
            if(popupBlock.classList.contains('submit-popup-categories')) {
               const activeItems = popupBlock.querySelectorAll('.-categories-li.-active')
               if (activeItems.length > 0) {
                  activeItems.forEach(activeItem => {
                     const activeCol = activeItem.querySelector('.-categories-col.-open')
                     activeCol.classList.remove('-open')
                     activeItem.classList.remove('-active')
                  })
               }
            }
            thisClass.closePopup(popupBlock)
         }
      }
   }
   openPopup(el, anim = true) {
      el.classList.add('-open')
      el.classList.add('-anim')
      setTimeout(() => {
         el.classList.remove('-anim')
      }, 400)
      if (anim) {
         this.actionPadding()
         document.body.classList.add('-lock-popup')
      }
   }
   closePopup(el) {
      el.classList.add('-anim')
      el.classList.remove('-open')
      setTimeout(() => {
         this.actionPadding(false)
         document.body.classList.remove('-lock-popup')
         el.classList.remove('-anim')
      }, 400)
   }
   actionPadding(addPadding = true) {
      const arrPaddingElements = []
      arrPaddingElements.push(document.body)
      
      const paddingElements = document.querySelectorAll('.-popup-padding')
      if (paddingElements.length > 0) {
         paddingElements.forEach(el => arrPaddingElements.push(el))
      }
      if (addPadding) {
         const widthScrollBar = window.innerWidth - document.querySelector('.wrapper').offsetWidth;
         arrPaddingElements.forEach(element => {
            element.style.paddingRight = widthScrollBar + 'px'
         })
      } else {
         arrPaddingElements.forEach(element => {
            element.style.paddingRight = ''
         })
      }
   }
}
const popup = new Popup()
popup.init()

const isMobile = {
   Android: function () { return navigator.userAgent.match(/Android/i); },
   BlackBerry: function () { return navigator.userAgent.match(/BlackBerry/i); },
   iOS: function () { return navigator.userAgent.match(/iPhone|iPad|iPod/i); },
   Opera: function () { return navigator.userAgent.match(/Opera Mini/i); },
   Windows: function () { return navigator.userAgent.match(/IEMobile/i); },
   any: function () { return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows()); }
};

document.addEventListener('click', actionDocument)
const headerElement = document.querySelector('.header')
function actionDocument(e) {
   const target = e.target;
   if (target.closest('.burger-header')) {
      const burgerMenu = target.closest('.burger-header')
      const menu = document.querySelector('.menu')
      burgerMenu.classList.add('-active')
      menu.classList.add('-open')
      headerElement.classList.add('-active')
      document.body.classList.add('-lock')
   }
   if (target.closest('.menu__close')) {
      e.preventDefault()
      const menuClose = target.closest('.menu__close')
      const burgerMenu = document.querySelector('.burger-header')
      const menu = document.querySelector('.menu')
      burgerMenu.classList.remove('-active')
      menu.classList.remove('-open')
      headerElement.classList.remove('-active')
      document.body.classList.remove('-lock')
   }
   if (target.closest('.form-filter__close')) {
      e.preventDefault()
      const formFilter = document.querySelector('.form-filter')
      formFilter.classList.remove('-open')
      document.body.classList.remove('-lock-filter')
      if (target.closest('.form-filter__close').classList.contains('form-filter__close_lock')) {
         document.body.classList.remove('-lock-filter-l')
      }
   }
   if (target.closest('.filter-openner')) {
      e.preventDefault()
      if (window.innerWidth < '767.98') {
         const formFilter = document.querySelector('.form-filter')
         formFilter.classList.add('-open')
         document.body.classList.add('-lock-filter')
         if (target.closest('.filter-openner').classList.contains('filter-openner_lock')) {
            document.body.classList.add('-lock-filter-l')
         }
      }
   }
   if (target.closest('.tooltip-form-filter__icon') && isMobile.any()) {
      const tooltipIcon = target.closest('.tooltip-form-filter__icon')
      tooltipIcon.nextElementSibling.classList.toggle('-open')
   } else if (!target.closest('.tooltip-form-filter') && isMobile.any()) {
      const tooltipIcon = document.querySelector('.tooltip-form-filter__icon')
      if (tooltipIcon) {
         tooltipIcon.nextElementSibling.classList.remove('-open')
      }
   }
   if (target.closest('.item-message-profile__openner')) {
      e.preventDefault()
      const itemMessageProfile = target.closest('.item-message-profile__openner')
      const chatsElement = itemMessageProfile.parentElement.nextElementSibling
      chatsElement.classList.add('-open')
      const chatsScrollElement = chatsElement.querySelector('.chat-item-message-profile__main')
      chatsScrollElement.querySelector('[data-scroll-wrap]').scrollTo({
         top: chatsScrollElement.offsetHeight
      })
   }
   if (target.closest('.chat-item-message-profile__close')) {
      e.preventDefault()
      const chatMessageClose = target.closest('.chat-item-message-profile__close')
      chatMessageClose.closest('.chat-item-message-profile').classList.remove('-open')
   }
   if (target.closest('.message-error-profile__close')) {
      e.preventDefault()
      const messageErrorClose = target.closest('.message-error-profile__close')
      messageErrorClose.closest('.message-error-profile').classList.remove('-active')
   }
   if (target.closest('.-categories-li')) {
      const categoriesLi = target.closest('.-categories-li')

      if (!categoriesLi.classList.contains('-categories-li-no')) {
         const categoriesList = categoriesLi.closest('.-categories-list')
         const categoriesItems = Array.from(categoriesList.children)
         if (categoriesLi.classList.contains('-categories-li_list')) {
            const activeItems = categoriesList.querySelectorAll('.-categories-li.-active')
            if (activeItems.length > 0) {
               activeItems.forEach(activeItem => {
                  const activeCol = activeItem.querySelector('.-categories-col.-open')
                  activeCol.classList.remove('-open')
                  activeItem.classList.remove('-active')
               })
            }

         }
         categoriesItems.forEach(item => {
            item.classList.remove('-active')
            item.querySelector('.-categories-col').classList.remove('-open')
         })
         categoriesLi.classList.add('-active')
         categoriesLi.querySelector('.-categories-col').classList.add('-open')
      }
   }
   if (target.closest('.-close-col')) {
      e.preventDefault()
      const colClose = target.closest('.-close-col')
      colClose.closest('.-categories-col').classList.remove('-open')
      colClose.closest('.-categories-li').classList.remove('-active')
   }
   if (target.closest('.-btn-review-input-show')) {
      e.preventDefault()
      const formReviewBtn = target.closest('.-btn-review-input-show')
      formReviewBtn.nextElementSibling.classList.add('-show')
      formReviewBtn.closest('.form-review').classList.add('-show')
      slideDown(document.querySelector('.form-review__body'))
      setTimeout(() => {
         formReviewBtn.classList.add('-hide')
         ssb.refresh()
      }, 400);
   }
   if (target.closest('.language-select__openner')) {
      setTimeout(() => {
         ssb.refresh()
      }, 400);
   }
   if (target.closest('.prices-list-product__more')) {
      e.preventDefault()
      const btnListMore = target.closest('.prices-list-product__more')
      const pricesListBody = document.querySelector('.prices-list-product__body')
      if (pricesListBody) {
         const pricesListItemsAdd = pricesListBody.querySelectorAll('.prices-list-product__item.-add-price')
         if (pricesListItemsAdd.length > 0) {
            pricesListItemsAdd.forEach(pricesListItem => {
               pricesListItem.classList.remove('-add-price')
            })
            btnListMore.remove()
         }
      }
   }
   if (!target.closest('.profile-header')) {
      const profileHeaderProfile = document.querySelector('.profile-header__profile')
      if (profileHeaderProfile) {
         if (profileHeaderProfile.classList.contains('-active')) {
            profileHeaderProfile.click()
         }
      }
   }
   if (!target.closest('[data-menu-add-li]')) {
      const btnMenuAdd = document.querySelector('[data-menu-add]')
      if (btnMenuAdd) {
         if (btnMenuAdd.classList.contains('-active')) {
            btnMenuAdd.click()
         }
      }
   }
}
const searchFooter = document.querySelector('.search-footer')
if (searchFooter) {
   new ValidateForm(searchFooter, {
      method: 'GET',
      url: '',
      items: {
         input: searchFooter.querySelectorAll('input[type="text"].-req'),
      }
   })
}
const searchForm = document.querySelector('.search__row')
if (searchForm) {
   new ValidateForm(searchForm, {
      method: 'GET',
      url: '',
      items: {
         input: searchForm.querySelectorAll('input[type="text"].-req, input[type="date"].-req'),
      }
   })
}

const mqlSlider = window.matchMedia('(min-width: 767.98px)')
function disableSlider(slider, classSlider, settings) {
   function start(e) {
      if (e.matches) {
         if (!slider) {
            slider = new Swiper(classSlider, settings)
         }
      } else {
         if (slider) {
            slider.destroy()
            slider = null
         }
      }
   }
   if (document.querySelector(classSlider)) {
      start(mqlSlider)
      mqlSlider.addEventListener('change', e => {
         start(e)
      })
   }
}
let sliderBest = null
disableSlider(sliderBest, '.slider-best__body', {
   navigation: {
      nextEl: '.slider-best__arrows .arrows-slider-big__arrow_next',
      prevEl: '.slider-best__arrows .arrows-slider-big__arrow_prev'
   },
   simulateTouch: true,
   grabCursor: true,
   slidesPerView: 2,
   watchOverflow: false,
   spaceBetween: 30,
})

const mainSliderProduct = new Swiper('.main-slider-product__body', {
   navigation: {
      nextEl: '.main-slider-product__arrows .arrows-slider__arrow_next',
      prevEl: '.main-slider-product__arrows .arrows-slider__arrow_prev'
   },
   simulateTouch: true,
   grabCursor: true,
   watchOverflow: false,
})
const submainSliderProduct = new Swiper('.submain-slider-product__body', {
   navigation: {
      nextEl: '.submain-slider-product__arrows .arrows-slider__arrow_next',
      prevEl: '.submain-slider-product__arrows .arrows-slider__arrow_prev'
   },
   simulateTouch: true,
   grabCursor: true,
   watchOverflow: false,
   spaceBetween: 10,
   breakpoints: {
      0: {
         slidesPerView: 2,
      },
      575.98: {
         slidesPerView: 3,
      },
      767.98: {
         slidesPerView: 4,
      }
   }
})

mainSliderProduct.controller.control = submainSliderProduct
submainSliderProduct.controller.control = mainSliderProduct

const formContactProduct = document.querySelector('.form-contact-product')
if (formContactProduct) {
   new ValidateForm(formContactProduct, {
      method: 'GET',
      url: '',
      items: {
         input: formContactProduct.querySelectorAll('input[type="text"].-req, textarea.-req'),
      }
   })
}
const sliderSuggestionsProduct = new Swiper('.slider-suggestions-product__body', {
   pagination: {
      el: '.slider-suggestions-product__pagination',
      clickable: true,
   },
   simulateTouch: true,
   grabCursor: true,
   watchOverflow: false,
})


let sliderSimilarAds = null
disableSlider(sliderSimilarAds, '.slider-similar-ads__body', {
   navigation: {
      nextEl: '.slider-similar-ads__arrows .arrows-slider__arrow_next',
      prevEl: '.slider-similar-ads__arrows .arrows-slider__arrow_prev'
   },
   simulateTouch: true,
   grabCursor: true,
   watchOverflow: false,
   spaceBetween: 30,
   slidesPerView: 4,
   slidesPerGroup: 4,
   breakpoints: {
      0: {
         slidesPerView: 1,
         slidesPerGroup: 1,
      },
      575.98: {
         slidesPerView: 2,
         slidesPerGroup: 2,
      },
      991.98: {
         slidesPerView: 3,
         slidesPerGroup: 3,
      },
      1247.98: {
         slidesPerView: 4,
         slidesPerGroup: 4,
      },
   }
})


const slidersArticlesSide = document.querySelectorAll('.slider-articles-item-side__body')
if (slidersArticlesSide.length > 0) {
   slidersArticlesSide.forEach(slider => {
      const sliderArticlesSide = new Swiper(slider, {
         pagination: {
            el: slider.nextElementSibling,
            clickable: true,
         },
         simulateTouch: true,
         grabCursor: true,
         watchOverflow: false,
      })

   })
}

const formCommentsNewsSingle = document.querySelector('.form-comments-news-single')
if (formCommentsNewsSingle) {
   new ValidateForm(formCommentsNewsSingle, {
      method: 'GET',
      url: '',
      items: {
         input: formCommentsNewsSingle.querySelectorAll('input[type="text"].-req, textarea.-req'),
      }
   })
}

const rangeFormFilter = document.querySelector('.range-form-filter__slider');

if (rangeFormFilter) {
   noUiSlider.create(rangeFormFilter, {
      start: [0, 10000],
      connect: true,
      range: {
         'min': 0,
         'max': 10000
      },
      format: {
         from: function (value) {
            return parseInt(value);
         },
         to: function (value) {
            return parseInt(value);
         }
      }
   })
   const rangeFormFilterMin = document.querySelector('.range-form-filter__label_min'),
      rangeFormFilterMax = document.querySelector('.range-form-filter__label_max');

   rangeFormFilter.noUiSlider.on('update', function (values, handle) {
      if (handle) {
         rangeFormFilterMax.innerHTML = `$${values[handle].toLocaleString('en-US')}`
      } else {
         rangeFormFilterMin.innerHTML = `$${values[handle].toLocaleString('en-US')}`
      }
   });

   const priceStart = document.getElementById('price-start')
   const priceEnd = document.getElementById('price-end')
   priceStart.addEventListener('change', setPriceValues)
   priceEnd.addEventListener('change', setPriceValues)
   function setPriceValues() {
      let priceStartValue;
      let priceEndValue;
      if (priceStart.value != '') {
         priceStartValue = priceStart.value.replace('$', '')
      }
      if (priceEnd.value != '') {
         priceEndValue = priceEnd.value.replace('$', '')
      }
      rangeFormFilter.noUiSlider.set([priceStartValue, priceEndValue])
   }
}

function removeLockBody(e) {
   if (!e.matches) {
      document.body.classList.remove('-lock-filter')
   }
}
removeLockBody(mqlSlider)
mqlSlider.addEventListener('change', e => removeLockBody(e))

const formCommentsProduct = document.querySelector('.form-comments-product')
if (formCommentsProduct) {
   new ValidateForm(formCommentsProduct, {
      method: 'GET',
      url: '',
      items: {
         input: formCommentsProduct.querySelectorAll('textarea.-req'),
      }
   })
}

const loginForm = document.querySelector('.login-form')
if (loginForm) {
   new ValidateForm(loginForm, {
      method: 'GET',
      url: '',
      items: {
         input: loginForm.querySelectorAll('input[type="text"].-req, input[type="number"].-req, input[type="password"].-req'),
         checkbox: loginForm.querySelectorAll('input[type="checkbox"].-req'),
      }
   })
}

function setActivePasswordLabel(label) {
   label.classList.add('-active')
}
function removeActivePasswordLabel(label) {
   label.classList.remove('-active')
}

const inputsPasswordValid = document.querySelectorAll('.-password-valid')
if (inputsPasswordValid.length > 0) {
   inputsPasswordValid.forEach(input => {
      const validLabel = input.parentElement.nextElementSibling
      validLabel.innerHTML = `
      <span>A</span><span>-</span><span>a</span><span>-</span><span>123</span><span>-</span><span>.,</span>
      `
      input.addEventListener('keyup', function () {
         if (!regexPasswordValid.test(input.value)) {
            const labelUpCase = validLabel.querySelectorAll('*')[0]
            const labelDownCace = validLabel.querySelectorAll('*')[2]
            const labelNum = validLabel.querySelectorAll('*')[4]
            const labelSpecial = validLabel.querySelectorAll('*')[6]

            if (/(?=.*[A-Z])/.test(input.value)) {
               setActivePasswordLabel(labelUpCase)
            } else {
               removeActivePasswordLabel(labelUpCase)
            }
            if (/(?=.*[a-z])/.test(input.value)) {
               setActivePasswordLabel(labelDownCace)
            } else {
               removeActivePasswordLabel(labelDownCace)
            }
            if (/(?=.*[0-9])/.test(input.value)) {
               setActivePasswordLabel(labelNum)
            } else {
               removeActivePasswordLabel(labelNum)
            }
            if (/(?=.*[!@#$%^&*])/.test(input.value)) {
               setActivePasswordLabel(labelSpecial)
            } else {
               removeActivePasswordLabel(labelSpecial)
            }

            const linesLabel = Array.from(validLabel.querySelectorAll('span')).filter(label => label.textContent == '-')
            if (linesLabel.length > 0) {
               linesLabel.forEach(lineLabel => {
                  const previousLabel = lineLabel.previousElementSibling
                  const nextLabel = lineLabel.nextElementSibling
                  if (previousLabel.classList.contains('-active') && nextLabel.classList.contains('-active')) {
                     lineLabel.classList.add('-active')
                  } else {
                     lineLabel.classList.remove('-active')
                  }
               })
            }
         } else {
            validLabel.querySelectorAll('*').forEach(label => label.classList.add('-active'))
         }
      })
   })
}
const formsChatItemMessageProfile = document.querySelectorAll('.form-chat-item-message-profile')
if (formsChatItemMessageProfile.length > 0) {
   formsChatItemMessageProfile.forEach(formChatMessage => {
      new ValidateForm(formChatMessage, {
         method: 'GET',
         url: '',
         items: {
            input: formChatMessage.querySelectorAll('textarea.-req'),
         }
      })
   })
}

const formsSettingsProfile = document.querySelectorAll('.form-settings-profile')
if (formsSettingsProfile.length > 0) {
   formsSettingsProfile.forEach(formSettingsProfile => {
      new ValidateForm(formSettingsProfile, {
         method: 'GET',
         url: '',
         items: {
            input: formSettingsProfile.querySelectorAll('input.-req, input[type="file"]'),
         }
      })
   })
}

const formWalletProfile = document.querySelector('.form-wallet-profile')
if (formWalletProfile) {
   new ValidateForm(formWalletProfile, {
      method: 'GET',
      url: '',
      items: {
         input: formWalletProfile.querySelectorAll('input[type="number"].-req, input[type="text"].-req'),
      }
   })
}
const submitDetailForm = document.querySelector('.submit-detail__form')
if (submitDetailForm) {
   new ValidateForm(submitDetailForm, {
      method: 'GET',
      url: '',
      items: {
         input: submitDetailForm.querySelectorAll('input[type="text"].-req, input[type="number"].-req, textarea.-req'),
         checkbox: submitDetailForm.querySelectorAll('input[type="checkbox"].-req'),
         file: submitDetailForm.querySelectorAll('input[type="file"].-req'),
      }
   })
}

const inputMessageReview = document.querySelector('.form-review__body')
if (inputMessageReview) {
   slideUp(inputMessageReview, 0)
}

const formReview = document.querySelector('.form-review')
if (formReview) {
   new ValidateForm(formReview, {
      method: 'GET',
      url: '',
      items: {
         input: formReview.querySelectorAll('textarea.-req'),
      }
   })
}

const pageEl = document.querySelector('.page')
if (pageEl) {
   function setPaddingPageEl() {
      pageEl.style.paddingTop = document.querySelector('.header').offsetHeight + 'px'
   }
   setPaddingPageEl()
   window.addEventListener('resize', setPaddingPageEl)
}

const slidersItemProductsAds = document.querySelectorAll('.slider-item-products-ads__body')
if (slidersItemProductsAds.length > 0) {
   slidersItemProductsAds.forEach(slider => {
      const sliderPagination = slider.nextElementSibling
      const sliderItemProductsAds = new Swiper(slider, {
         simulateTouch: false,
         watchOverflow: false,
         nexted: true,
         pagination: {
            el: sliderPagination,
            clickable: true,
            renderBullet: function (index, className) {
               return `<div class="${className}" data-dots="${index}"><span></span></div>`
            }
         },
         breakpoints: {
            0: {
               pagination: {
                  clickable: true
               }
            },
            991.98: {
               pagination: {
                  clickable: false
               }
            }
         }
      })
      if (!isMobile.any()) {
         const dotsSlider = sliderPagination.querySelectorAll('.swiper-pagination-bullet')
         if (dotsSlider.length > 0) {
            dotsSlider.forEach(item => {
               item.addEventListener('mousemove', () => {
                  sliderItemProductsAds.slideTo(item.dataset.dots, 600)
               })
            })
         }
      }
   })
}

const formFilter = document.querySelector('.form-filter')
if (formFilter) {
   new ValidateForm(formFilter, {
      method: 'GET',
      url: '',
      items: {
         input: formFilter.querySelectorAll('input[type="number"].-req'),
         checkbox: formFilter.querySelectorAll('input[type="checkbox"].-req'),
         radio: formFilter.querySelectorAll('input[type="radio"].-req'),
      }
   })
}
const formArticles = document.querySelector('.form-articles')
if (formArticles) {
   new ValidateForm(formArticles, {
      method: 'GET',
      url: ''
   })
}
const ratings = document.querySelectorAll('.rating-review_user')
if (ratings.length > 0) {
   initRatings()
}
function initRatings() {
   let ratingActive, ratingValue;
   for (let index = 0; index < ratings.length; index++) {
      const rating = ratings[index];
      initRating(rating)
   }
   function initRating(rating) {
      initRatingVars(rating)

      setRatingActiveWidth()

      setRating(rating)
   }

   function initRatingVars(rating) {
      ratingActive = rating.querySelector('.rating-review__active')
      ratingValue = rating.querySelector('.rating-review__label')
   }
   function setRatingActiveWidth(index = ratingValue.innerHTML) {
      const ratingActiveWidth = index / 0.05
      ratingActive.style.width = `${ratingActiveWidth}%`
   }
   function setRating(rating) {
      const ratingsItems = rating.querySelectorAll('.rating-review__input')
      for (let index = 0; index < ratingsItems.length; index++) {
         const ratingItem = ratingsItems[index];
         console.log(ratingItem);
         ratingItem.addEventListener('mouseenter', () => {
            initRatingVars(rating)
            setRatingActiveWidth(ratingItem.value)
         })
         ratingItem.addEventListener('mouseleave', () => {
            setRatingActiveWidth()
         })
         ratingItem.addEventListener('click', () => {
            initRatingVars(rating)
            ratingValue.innerHTML = index + 1
            setRatingActiveWidth()
         })
      }
   }
}