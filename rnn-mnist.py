import tensorflow as tf 
from tensorflow.python.ops import rnn, rnn_cell
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/tmp/data", one_hot = True)

hm_epochs = 10
n_classes = 10
batch_size = 128
no_chunks = 28
chunk_size = 28
rnn_size = 128

x = tf.placeholder('float', [None, no_chunks, chunk_size])
y = tf.placeholder('float')



def recurrent_network_model(x):

	layer = {'weight':tf.Variable(tf.random_normal([rnn_size, n_classes])), 'biases':tf.Variable(tf.random_normal([n_classes]))}
	
	x = tf.transpose(x, [1,0,2])
	x = tf.reshape(x, [-1, chunk_size])
	x = tf.split(x, no_chunks, 0)

	#See these two line in detail...
	lstm_cell = rnn_cell.BasicLSTMCell(rnn_size,state_is_tuple=True)
	outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

	
	output = tf.add( tf.matmul(outputs[-1], layer['weight']) , layer['biases'] )

	return output

def train_neural_network(x):

	prediction = recurrent_network_model(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		for epoch in range(hm_epochs):
			epoch_loss = 0
			for _ in range(int(mnist.train.num_examples/batch_size)):
                                
				epoch_x, epoch_y = mnist.train.next_batch(batch_size)
				epoch_x = epoch_x.reshape((batch_size,no_chunks,chunk_size))

				_, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
				epoch_loss += c
				#print('Epoch', epoch, 'completed out of',hm_epochs,'cost:',c)


			print('-----------------------------------------------------')
			print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)
			
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		print('Accuracy:',accuracy.eval({x:mnist.test.images.reshape(-1,no_chunks,chunk_size), y:mnist.test.labels}))

train_neural_network(x)






























