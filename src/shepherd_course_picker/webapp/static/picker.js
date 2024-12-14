var Cart = []
const CartElement = document.getElementsByClassName('cart')[0] // TODO use ID

const TotalElement = document.getElementById('total_credits')

function array_remove(array, target) {
    const index = array.indexOf(target);
    if (index !== -1) {
        array.splice(index, 1)
    }
}

function array_in(array, target) {
    return array.indexOf(target) > -1
}


function updateCart(node) {
    // Node is already in cart. remove it
    if (array_in(Cart, node)) {
        array_remove(Cart, node)
        CartElement.removeChild(node.cartElement)

        node.pickerElement.classList.remove("in_cart")
    }

    // Add node to cart
    else {
        Cart.push(node)
        CartElement.appendChild(
            node.cartElement
        )

        node.pickerElement.classList.add("in_cart")


    }


    let total = 0
    Cart.forEach(node => {
        total += node.credits
    })
    TotalElement.textContent = `Total Credits: ${total}`
}

class Node {

    makeElement(input_data) {
        // Create HTML element:

        // Create a new DOM element for myself!
        let new_element = document.createElement('div')

        new_element.classList.add('node');

        // For styling purposes (CSS is too hard)
        new_element.setAttribute('depth', this.depth);

        // Set my title
        new_element.textContent = input_data['name']

        // Node has credit and therefore should be clickable
        if (this.credits) {
            new_element.classList.add('clickable_node');
            new_element.onclick = () => {
                updateCart(this)
            }
        }

        // Node has some text
        if (input_data['text']) {
            input_data['text'].forEach(text => {
                let new_child_element = document.createElement('p')
                new_child_element.textContent = text
                new_element.appendChild(
                    new_child_element
                )
            })
        }

        return new_element
    }

    // Right side of page
    makeCartElement() {
        let element_to_return = this.element.cloneNode(true)

        element_to_return.onclick = this.element.onclick

        return element_to_return

    }

    // Left side of page
    makePickerElement() {
        let element_to_return = this.element.cloneNode(true)
        element_to_return.onclick = this.element.onclick // for some reason the on click doesnt work when copied from this.element

        this.childNodes.forEach(child_node => {
            element_to_return.appendChild(
                child_node.pickerElement
            )
        })


        return element_to_return
    }


    constructor(input_data, depth = 0) {
        // Data about the node

        this.depth = depth

        this.childNodes = [] // Empty list of children

        // Recursively append my (NODE) children to myself
        if (input_data['nodes']) {
            input_data['nodes'].forEach(child_data => {
                    let newone = new Node(
                        child_data,
                        (this.depth === 1 ? 0 : 1)
                    )
                    this.appendChildNode(newone)
                }
            );
        }

        if (input_data['credits']) {
            this.credits = input_data['credits']
        }


        this.element = this.makeElement(input_data)

        this.pickerElement = this.makePickerElement()
        this.cartElement = this.makeCartElement()


    }

    appendChildNode(node) {
        this.childNodes.push(
            node
        )
    }

}

var rootNode = null

document.addEventListener("DOMContentLoaded", () => {
    // Function to fetch data from the server
    async function fetchData() {
        // Send a GET request to the server
        const response = await fetch(`/api/programs/${program_id}`);

        // Parse the JSON response
        const data = await response.json();
        if (data['error']) {
            throw new Error(data['error'])
        } else {


            // console.log(data)
            rootNode = new Node(
                data
            )

            document.getElementsByClassName("node")[0].appendChild(
                rootNode.pickerElement
            )

        }
    }

    // Fetch data when the page loads
    fetchData().catch(error =>
    {
        // This block runs if an error is thrown
        alert(`Something went wrong.\nSomething: \"${error}\"`)
        window.location = '/'
    })

});
