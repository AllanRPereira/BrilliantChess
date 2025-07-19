<script setup>
import {ref, onMounted, computed} from 'vue';
import { Chess } from 'chess.js';
import {chessboard} from 'vue-chessboard';
import 'vue-chessboard/dist/vue-chessboard.css';

const chess = new Chess();
const boardAPI = ref(null); // TO DO
const boardConfig = ref({
    fen: 'start', // Posicao inicial p/ser analisada
    viewOnly: true, // Por enquanto só visualização
})